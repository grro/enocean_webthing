import sys
from time import sleep
from typing import List
from webthing import (MultipleThings, Property, Thing, Value, WebThingServer)
from device import Enocean, WindowHandle, DeviceListener
import logging
import tornado.ioloop


class WindowHandleWebThing(Thing, DeviceListener):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, description: str, name: str, directory: str, eep_id: str, enocean_id: str):
        Thing.__init__(
            self,
            'urn:dev:ops:window-handle-1',
            'WindowHandle ' + name,
            ['MultiLevelSensor'],
            description
        )

        self.ioloop = tornado.ioloop.IOLoop.current()

        self.device = WindowHandle(name, directory, eep_id, enocean_id, self)

        self.name = Value(name)
        self.add_property(
            Property(self,
                     'name',
                     self.name,
                     metadata={
                         'title': 'name',
                         "type": "string",
                         'description': '"The name',
                         'readOnly': True,
                     }))

        self.eepid = Value(eep_id)
        self.add_property(
            Property(self,
                     'eep_id',
                     self.eepid,
                     metadata={
                         'title': 'eep id',
                         "type": "string",
                         'description': '"The eep id',
                         'readOnly': True,
                     }))

        self.enoceanid = Value(enocean_id)
        self.add_property(
            Property(self,
                     'enocean_id',
                     self.enoceanid,
                     metadata={
                         'title': 'enocean id',
                         "type": "string",
                         'description': '"The enocean id',
                         'readOnly': True,
                     }))

        self.state = Value(self.device.state)
        self.add_property(
            Property(self,
                     'state',
                     self.state,
                     metadata={
                         'title': 'State',
                         "type": "integer",
                         'description': 'The state of the handle',
                         'readOnly': True,
                     }))

        self.state_text = Value(self.device.state_text)
        self.add_property(
            Property(self,
                     'state_text',
                     self.state_text,
                     metadata={
                         'title': 'State Description',
                         "type": "string",
                         'description': 'The state description',
                         'readOnly': True,
                     }))

        self.closed = Value(self.device.closed)
        self.add_property(
            Property(self,
                     'closed',
                     self.closed,
                     metadata={
                         'title': 'Closed state',
                         "type": "boolean",
                         'description': 'True, if closed',
                         'readOnly': True,
                     }))

    def on_updated(self, device: WindowHandle):
        self.ioloop.add_callback(self.__update_state, device)

    def __update_state(self, device: WindowHandle):
        self.state.notify_of_external_update(device.state)
        self.state_text.notify_of_external_update(device.state_text)
        self.closed.notify_of_external_update(device.closed)

def run_server(description: str, directory: str, port: int, path: str, addresses: List[str]):
    enocean_webthings = []
    for address in sorted(addresses):
        name, eep_id, enocean_id = address.split("/")
        if WindowHandle.supports(eep_id):
            enocean_webthings.append(WindowHandleWebThing(description, name, directory, eep_id, enocean_id))
        else:
            logging.warning("unsupported device (eep_id: " + eep_id + ", enocean_id: " + enocean_id +"). Ignoring it")

    enocean = Enocean(path, [enocean_webthing.device for enocean_webthing in enocean_webthings])
    server = WebThingServer(MultipleThings(enocean_webthings, 'devices'), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server (port: ' + str(port) + ')')
        enocean.receive(background=True)
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        enocean.stop()
        logging.info('done')
        return
    except Exception as e:
        logging.error(e)
        sleep(3)




if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('tornado.access').setLevel(logging.ERROR)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    run_server("description", sys.argv[1], int(sys.argv[2]), sys.argv[3], [addr.strip() for addr in sys.argv[4].split(",")])


