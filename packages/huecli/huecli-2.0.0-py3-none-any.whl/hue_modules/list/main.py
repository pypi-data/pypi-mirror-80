from clilib.util.util import Util
from clilib.util.arg_tools import arg_tools
from hue_modules.util.bridge import Bridge
import json


class main:
    def __init__(self):
        self.spec = {
            "desc": 'List available lights',
            "name": 'list',
            "positionals": [],
            "flags": [
                {
                    "names": ['-d', '--debug'],
                    "help": "Add extended output.",
                    "required": False,
                    "default": False,
                    "action": "store_true",
                    "type": bool
                },
                {
                    "names": ['-a', '--address'],
                    "help": "IP address of the Hue bridge",
                    "required": False,
                    "type": str,
                    "default": "192.168.1.1"
                }
            ]
        }
        args = arg_tools.build_full_subparser(self.spec)
        self.args = args
        self.logger = Util.configure_logging(args, __name__)
        self.print_lights()

    def print_lights(self):
        self.logger.debug("Connecting to Hue bridge on %s" % self.args.address)
        b = Bridge.init_bridge(self.args.address)
        print("ID\tLight Name\r\n----------------------")
        lights = b.get_light_objects('id')
        for id, light in lights.items():
            print("%d\t%s" % (id, light.name))

        print("\r\nID\tGroup Name\r\n----------------------")
        groups = b.get_group()
        for group in groups:
            print("%d\t%s" % (int(group), b.get_group(int(group), 'name')))
