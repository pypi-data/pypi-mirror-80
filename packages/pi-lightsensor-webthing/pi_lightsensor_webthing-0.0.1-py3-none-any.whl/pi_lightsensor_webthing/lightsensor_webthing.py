from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
import logging
import tornado.ioloop
import RPi.GPIO as GPIO


class LightSensor(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, gpio_number, description):
        Thing.__init__(
            self,
            'urn:dev:ops:illuminanceSensor-1',
            'IlluminanceSensor',
            [''],
            description
        )

        self.gpio_number = gpio_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.IN)

        self.bright = Value(False)
        self.add_property(
            Property(self,
                     'bright',
                     self.bright,
                     metadata={
                         '@type': 'OnOffProperty',
                         'title': 'bright',
                         "type": "boolean",
                         'description': 'Is bright',
                         'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.measure,
            60000
        )
        self.measure()
        self.timer.start()

    def measure(self):
        if GPIO.input(self.gpio_number):
            self.bright.notify_of_external_update(True)
        else:
            self.bright.notify_of_external_update(True)

    def cancel_update_level_task(self):
        self.timer.stop()


def run_server(port, gpio_number, description):
    light_sensor = LightSensor(gpio_number, description)
    server = WebThingServer(SingleThing(light_sensor), port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        light_sensor.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

