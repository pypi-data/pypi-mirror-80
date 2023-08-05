from clilib.util.util import Util
from clilib.util.arg_tools import arg_tools
from hue_modules.util.bridge import Bridge


class main:
    def __init__(self):
        self.spec = {
            "desc": 'Change color of lights',
            "name": 'color',
            "positionals": [
                {
                    "name": "id",
                    "metavar": "ID",
                    "help": "ID of the light or group to manipulate.",
                    "type": int,
                    "default": False
                },
                {
                    "name": "color",
                    "metavar": "COLOR",
                    "help": "Hex color to change light to.",
                    "type": str,
                    "default": "FFFFFF"
                }
            ],
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
        self.change_color()

    def change_color(self):
        b = Bridge.init_bridge(self.args.address)
        if self.args.group:
            b.set_group(int(self.args.id), 'xy', self.convert_color(self.args.color))
        else:
            b.set_light(int(self.args.id), 'xy', self.convert_color(self.args.color))

    @staticmethod
    def convert_color(hexCode):
        R = int(hexCode[:2], 16)
        G = int(hexCode[2:4], 16)
        B = int(hexCode[4:6], 16)

        total = R + G + B

        if R == 0:
            firstPos = 0
        else:
            firstPos = R / total

        if G == 0:
            secondPos = 0
        else:
            secondPos = G / total

        return [firstPos, secondPos]