UnicornHue
==========

This is my implementation of the Philips [Hue] light using a [Raspberry Pi Zero] and a [Pimoroni]  GPIO add on board called the [UnicornHat]. It should look like the screenshot below when loaded up in a browser.

![Example Screenshot](/img/screenshot.png)

There are two bits of code, firstly the python demon designed to run on the pi (as root, so it can write to `/dev/mem`) and the web ui which is designed to be used in a browser.

The two communicate using the MQTT message protocol, I have the [Mosquitto] MQTT broker installed on my Pi, which must have WebSockets support enabled for this to work.  The HTML inside `index.html` loads settings from `config.js`, which tells it where the MQTT broker is, and which topic to post messages too. There are in the format of simple JSON documents which list the Red, Green, Blue and Alpha channel - I use the Alpha channel as the brightness.  An example message looks like:

```
{ "color": {"r":168,"g":136,"b":72,"a":0.5} }
```

I nested the color under the `color` property in case I wanted to expand it later.

color-changer.py
----------------

The python script `color-changer.py` is designed to run on the pi permanently, it uses environment variables for configuration. The options are:

* `MQTT_HOST` - The hostname of the MQTT broker
* `MQTT_TOPIC` - The topic to subscribe to messages for.
* `MQTT_USER` - Optional username if your broker requires it.
* `MQTT_PASSWORD` - Optional password, again if your broker requires it.

SupervisorD
-----------

I run the python out of the excellent [SupervisorD] process management utility, an example config file is included in `supervisor.d/color-changer`, on Ubuntu/Debian/Raspbian flavour distributions you should be able to install `supervisord` and configure it like so:

```
% sudo apt-get install supervisord
% sudo cp supervisor.d/color-changer /etc/supervisor/conf.d/
% sudo service supervisor restart
```

Supervisor will then load and try to run the `color-changer` program, logging to a file defined in the `stdout_logfile` entry in the supervisor config file included in this repo.

[Hue]: http://meethue.com/
[Raspberry Pi Zero]: https://www.raspberrypi.org/products/pi-zero/
[Pimoroni]: http://pimoroni.com/
[UnicornHat]: https://shop.pimoroni.com/products/unicorn-hat
[Mosquitto]: http://mosquitto.org/
[MQTT]: http://mqtt.org/
[SupervisorD]: http://supervisord.org/
