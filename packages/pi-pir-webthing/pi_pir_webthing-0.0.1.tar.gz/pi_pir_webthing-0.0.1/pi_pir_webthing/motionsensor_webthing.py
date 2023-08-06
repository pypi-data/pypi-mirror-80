from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
import logging
import RPi.GPIO as GPIO
from datetime import datetime


class MotionSensor(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, gpio_number, description):
        Thing.__init__(
            self,
            'urn:dev:ops:motionSensor-1',
            'MotionSensor',
            ['MotionSensor'],
            description
        )

        self.gpio_number = gpio_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.IN)
        GPIO.add_event_detect(self.gpio_number, GPIO.BOTH, callback=self.__update, bouncetime=5)

        self.motion = Value(False)
        self.add_property(
        Property(self,
                 'motion',
                 self.motion,
                 metadata={
                     '@type': 'MotionProperty',
                     'title': 'motion',
                     "type": "boolean",
                     'description': 'Whether motion is detected',
                     'readOnly': True,
                 }))

        self.last_motion = Value(datetime.now().isoformat())
        self.add_property(
            Property(self,
                     'last_motion',
                     self.last_motion,
                     metadata={
                         'title': 'last_motion',
                         "type": "datetime",
                         'description': 'The time of last movement',
                         'readOnly': True,
                     }))
        self.__update("")

    def __update(self, channel):
        is_motion = GPIO.input(self.gpio_number)
        logging.info("state updated: " + str(is_motion))
        if is_motion:
            self.motion.notify_of_external_update(True)
            self.last_motion.notify_of_external_update(datetime.now().isoformat())
        else:
            self.motion.notify_of_external_update(False)


def run_server(port, gpio_number, description):
    motion_sensor = MotionSensor(gpio_number, description)
    server = WebThingServer(SingleThing(motion_sensor), port=port)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

