import argparse
import os
import sys

import pkg_resources


class Cli(object):

    __VERSION_CMD = "python2" if sys.version_info[0] < 3 else "python3"

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage="""{invoke} COMMAND
                  Commands:
                  init\t Run this command to setup dependancies.
                  version\t Display current version
                  
                  Use: {} COMMAND -h to display COMMAND specific help
                  
                  """.format(Cli.__INVOCATION_CMD))
        parser.add_argument('command', help='command to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("[ERROR]\t\'{command}\' is not a {invoke} command\n"
                  .format(command=args.command, invoke=Cli.__INVOCATION_CMD))
            parser.print_help()
            exit(1)
        if args.command:
            getattr(self, args.command)()

    def init(self):

        if sys.platform in ["linux", "linux2"]:
            print("Initializing required component")
            pip = "pip" if sys.version_info[0] < 3 else "pip3"
            os.system('sudo apt-get -y install joystick')
            os.system('sudo apt install python-dev python3-dev python-pip python3-pip')
            #os.system('sudo {} install ds4drv'.format(pip))
            #os.system('sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules '
            #          '-O /etc/udev/rules.d/50-ds4drv.rules')
            os.system('sudo udevadm control --reload-rules')
            os.system('sudo udevadm trigger')
            print("Required distributions have successfully installed.")
        else:
            print("This package is only supported on Linux systems. Sorry!")

    def version(self):
        print("pyController {} (Python{})\n"
              .format(pkg_resources.require("pyController")[0].version, sys.version_info[0]))