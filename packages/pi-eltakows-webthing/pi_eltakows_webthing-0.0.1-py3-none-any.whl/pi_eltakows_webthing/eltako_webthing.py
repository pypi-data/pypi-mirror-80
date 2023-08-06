from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
import logging
import tornado.ioloop
import RPi.GPIO as GPIO


class EltakoWsSensor(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, gpio_number):
        Thing.__init__(
            self,
            'urn:dev:ops:eltakowsSensor-1',
            'Windsensor',
            [],
            'A web connected windsensor measuring wind speed'
        )

        self.gpio_number = gpio_number
        self.imp_per_15_sec = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.IN)
        GPIO.add_event_detect(self.gpio_number, GPIO.BOTH, callback=self.__spin, bouncetime=5)

        self.windspeed = Value(0.0)
        self.add_property(
            Property(self,
                     'windspeed',
                     self.windspeed,
                     metadata={
                         '@type': 'LevelProperty',
                         'title': 'Windspeed',
                         'type': 'number',
                         'description': 'The current windspeed',
                         'unit': 'km/h',
                         'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.measure,
            3000
        )
        self.timer.start()

    def __spin(self, channel):
        self.imp_per_15_sec += 1

    def measure(self):
        windspeed_kmh = self.__compute_speed_kmh(self.imp_per_15_sec / 15)
        self.imp_per_15_sec = 0
        self.windspeed.notify_of_external_update(windspeed_kmh)

    def __compute_speed_kmh(self, imp_per_sec):
        rotation_per_sec = imp_per_sec / 2
        km_per_hour = 1.761 / (1 + rotation_per_sec) + 3.813 * rotation_per_sec
        if km_per_hour < 2:
            km_per_hour = 0
        return round(km_per_hour,1)


    def cancel_update_level_task(self):
        self.timer.stop()


def run_server(port, gpio_number):
    eltakows_sensor = EltakoWsSensor(gpio_number)
    server = WebThingServer(SingleThing(eltakows_sensor), port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        eltakows_sensor.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

