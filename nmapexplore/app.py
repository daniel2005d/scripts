import argparse
import cmd2
from cmd2 import Cmd2ArgumentParser, with_argparser
from nmapexplore.db import DataBase

# show
# ports
# services
# hosts

class MainConsole(cmd2.Cmd):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, allow_cli_args=False, auto_load_commands=False)
        # self._workspace = kwargs["workspace"]
        # self._db = DataBase(self._workspace)
        self.prompt = f"nmap() > "
        
    def do_ports(self, args):
        ports = self._db.get_ports(self._workspace)
        print(ports)



parser = argparse.ArgumentParser()
parser.add_argument("-w","--workspace",help="Name of Workspace", type=str, required=True)
parser.add_argument("input",help="The XML file to be import",default=None, nargs="?")
parser.add_argument("--clean",help="Clean Database", action='store_true')
args = parser.parse_args()

main = MainConsole()
main.cmdloop()