from clilib.util.util import Util
from clilib.util.arg_tools import arg_tools
from phue import Bridge
import json


class main:
    def __init__(self):
        self.spec = {
            "desc": 'List available lights',
            "name": 'list'
        }
        parser, subparser = arg_tools.build_full_parser(self.spec)
        subparser.add_argument('-d', '--debug', help="Add extended output.", required=False, default=False,
                                   action='store_true')
        args = parser.parse_args()
        self.args = args
        self.args.logger = Util.configure_logging(args, __name__)
        self.print_lights()

    def print_lights(self):
        b = Bridge('192.168.1.136')

        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        b.connect()

        # Get the bridge state (This returns the full dictionary that you can explore)
        b.get_api()
        print("ID\tLight Name\r\n----------------------")
        lights = b.get_light_objects('id')
        for id,light in lights.items():
            print("%d\t%s" % (id, light.name))

        print("\r\nID\tGroup Name\r\n----------------------")
        groups = b.get_group()
        for group in groups:
            print("%d\t%s" % (int(group), b.get_group(int(group), 'name')))