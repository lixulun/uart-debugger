"""
处理python -m uart_debugger ...
"""

import getopt

argv = ""

def command_register(func, opts, long_opts):
    def new_func():
        pass

def list_ports():
    from winreg import OpenKey, EnumValue, QueryInfoKey, HKEY_LOCAL_MACHINE
    with OpenKey(HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\SERIALCOMM") as comm:
        count = QueryInfoKey(comm)[1]
        for i in range(count):
            name, value, _ = EnumValue(comm, i)
            print(name, value)