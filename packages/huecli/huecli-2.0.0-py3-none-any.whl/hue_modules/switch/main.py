from clilib.util.util import Util
from clilib.util.arg_tools import arg_tools
from hue_modules.util.bridge import Bridge
import json


class main:
    def __init__(self):
        self.command_methods = {
            'off': self.light_off,
            'on': self.light_on
        }
        self.spec = {
            "desc": 'Switch lights on and off. Supported subcommands are: {}'.format(", ".join(self.command_methods.keys())),
            "name": 'switch',
            "positionals": [
                {
                    "name": "subcommand",
                    "metavar": "SUBCOMMAND",
                    "help": "Subcommand for switch command.",
                    "default": "on",
                    "type": str
                },
                {
                    "name": "id",
                    "metavar": "ID",
                    "type": int,
                    "help": "ID of the light or group to manipulate.",
                    "default": False
                },
            ],
            "flags": [
                {
                    "names": ['-d', '--debug'],
                    "help": "Add extended output.",
                    "required": False,
                    "default": False,
                    "action": "store_true"
                },
                {
                    "names": ['-g', '--group'],
                    "help": "Switch group instead of individual light",
                    "required": False,
                    "default": False,
                    "action": "store_true"
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
        self.args.logger = Util.configure_logging(args, __name__)
        self.command_methods[args.subcommand]()

    def light_off(self):
        b = Bridge.init_bridge(self.args.address)
        if self.args.group:
            b.set_group(int(self.args.id), 'on', False)
        else:
            b.set_light(int(self.args.id), 'on', False)

    def light_on(self):
        b = Bridge.init_bridge(self.args.address)
        if self.args.group:
            b.set_group(int(self.args.id), 'on', True)
        else:
            b.set_light(int(self.args.id), 'on', True)
