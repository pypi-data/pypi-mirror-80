from clilib.util.util import Util
from clilib.util.arg_tools import arg_tools
from phue import Bridge
import json


class main:
    def __init__(self):
        self.command_methods = {
            'off': self.light_off,
            'on': self.light_on
        }
        self.spec = {
            "desc": 'Switch lights on and off. Supported subcommands are: {}'.format(", ".join(self.command_methods.keys())),
            "name": 'switch'
        }
        parser, subparser = arg_tools.build_full_parser(self.spec)
        subparser.add_argument('subcommand', metavar='SUBCOMMAND', help='Subcommand for switch command.', default=False)
        subparser.add_argument('id', metavar='ID', help='ID of the light or group to manipulate', type=int,
                               default=False)
        subparser.add_argument('-d', '--debug', help="Add extended output.", required=False, default=False,
                                   action='store_true')
        subparser.add_argument('-g', '--group', help="Switch group instead of light.", required=False, default=False,
                               action='store_true')
        args = parser.parse_args()
        self.args = args
        self.args.logger = Util.configure_logging(args, __name__)
        self.command_methods[args.subcommand]()

    def init_bridge(self):
        b = Bridge('192.168.1.136')

        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        b.connect()

        # Get the bridge state (This returns the full dictionary that you can explore)
        b.get_api()
        return b

    def light_off(self):
        b = self.init_bridge()
        if self.args.group:
            b.set_group(int(self.args.id), 'on', False)
        else:
            b.set_light(int(self.args.id), 'on', False)

    def light_on(self):
        b = self.init_bridge()
        if self.args.group:
            b.set_group(int(self.args.id), 'on', True)
        else:
            b.set_light(int(self.args.id), 'on', True)
