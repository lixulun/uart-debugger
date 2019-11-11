import sys
import getopt
from . import cli

def main():

    command = ""

    argv = sys.argv[1:]
    if not argv[0].startswith("-"):
        command = argv[0]
        argv = argv[1:]
    cli.argv = argv

    # try:
    #     opts, args = getopt.getopt(argv, "", [])
    #     for o, a in opts:
    #         pass
    # except getopt.GetoptError as err:
    #     print(err)
    #     usage()
    #     sys.exit(2)
    
    if command == "ports":
        cli.list_ports()

if __name__ == '__main__':
    main()