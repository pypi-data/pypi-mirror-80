from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pi_eltakows_webthing',
    packages=['pi_eltakows_webthing'],
    version_config={
        "version_format": "{tag}.dev{sha}",
        "starting_version": "0.0.1"
    },
    setup_requires=['better-setuptools-git-version'],
    description='A web connected Eltako windsensor measuring wind speed on Raspberry Pi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Gregor Roth',
    author_email='gregor.roth@web.de',
    url='https://github.com/grro/pi_eltakows_webthing',
    entry_points={
        'console_scripts': [
            'eltakows=pi_eltakows_webthing:main'
        ]
    },
    keywords=[
        'webthings', 'home automation', 'Eltako', 'windsensor', 'windspeed', 'WS', 'raspberry', 'pi'
    ],
    install_requires=[
        'webthing',
        'RPi.GPIO'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)

