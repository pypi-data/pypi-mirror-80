from clilib.util.util import Util
from clilib.util.arg_tools import arg_tools
from phue import Bridge
import json


class main:
    def __init__(self):
        self.spec = {
            "desc": 'Change color of lights',
            "name": 'color'
        }
        parser, subparser = arg_tools.build_full_parser(self.spec)
        subparser.add_argument('id', metavar='ID', help='ID of the light or group to manipulate', type=int,
                               default=False)
        subparser.add_argument('color', metavar='COLOR',  help='Hex color to change light to.', type=str, default=False)
        subparser.add_argument('-d', '--debug', help="Add extended output.", required=False, default=False,
                                   action='store_true')
        subparser.add_argument('-g', '--group', help="Use group instead of light.", required=False, default=False,
                               action='store_true')
        args = parser.parse_args()
        self.args = args
        self.args.logger = Util.configure_logging(args, __name__)
        self.change_color()

    def init_bridge(self):
        b = Bridge('192.168.1.136')

        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        b.connect()

        # Get the bridge state (This returns the full dictionary that you can explore)
        b.get_api()
        return b

    def change_color(self):
        b = self.init_bridge()
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