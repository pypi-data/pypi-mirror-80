# pi_eltakows_webthing
A web connected Eltako windsensor measuring wind speed on Raspberry Pi

This project provides a [webthing API](https://iot.mozilla.org/wot/) to a [Eltako windsensor](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_WS.pdf) 
running on a Raspberry Pi. As a webthing, the Eltako windsensor can be discovered and used by 
*home automation systems* or custom solutions supporting the webthing API.  

The pi_eltakows_webthing package exposes an http webthing endpoint which supports reading the wind speed via http. E.g. 
```
# webthing has been started on host 192.168.0.23

curl http://192.168.0.23:7050/properties 
{
   "windspeed": 2.6
}
```

Regarding the RaspberryPi/Eltako windsensor hardware setup and wiring please refer tutorials such as [Measure Wind Speed with Eltako Windsensor and Win10 IoT Core](https://www.hackster.io/daniel-kreuzhofer/measure-wind-speed-with-eltako-windsensor-and-win10-iot-core-e1e42a)

To install this software you may use [PIP](https://realpython.com/what-is-pip/) package manager such as shown below
```
sudo pip install pi_eltakows_webthing
```

After this installation you may start the webthing http endpoint inside your python code or via command line using
```
sudo eltakows --command listen --port 7050 --gpio 25
```
Here, the webthing API will be bind to the local port 7050 and be connected to the Eltako windsensor reed switch

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit. 
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary. 
```
sudo eltakows --command register --port 7050 --gpio 25
```  





