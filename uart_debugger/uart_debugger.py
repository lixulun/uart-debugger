import sys
import json
import time
import serial
import struct
import pdb
from collections import defaultdict
from threading import Thread


class TypeHandler:

    # 与struct.unpack参数相同
    _unpack_str = ""

    def __init__(self):
        self._count = 0
        # 上一次的时间 用户端不要使用这个属性
        self.__last_time = time.time()
        # 时间差(纳秒)
        self._timealpha = 0
        

    def __call__(self, data):
        self._count += 1
        self._timealpha = time.time() - self.__last_time
        self.__last_time = time.time()

class TypeDefine:

    def __init__(self, i_type, name, handler=None):
        self.name = name
        self.type = i_type
        self.handler = handler


class UartListener:

    def __init__(self):
        self._listeners = {}
        self._types = set()
        self._types_name = set()

    def register(self, td: TypeDefine):
        self._types.add(td.type)
        self._types_name.add(td.name)
        self._listeners[td.type] = td

    def have_type(self, type_i):
        return type_i in self._types

    def have_type_name(self, name):
        return name in self._types_name

    def get_handler(self, type_i):
        return self._listeners[type_i].handler

    def get_type_name(self, type_i):
        return self._listeners[type_i].name

    def get_unpack_str(self, type_i):
        if not self._listeners[type_i].__dict__.get("handler", None):
            return
        return self._listeners[type_i].handler.__dict__.get("_unpack_str", type(self._listeners[type_i].handler).__dict__.get("_unpack_str", None))

class UartDebugger(Thread):

    def __init__(self, listener: UartListener, *, port=None, baudrate=19200):
        super().__init__()
        # 设置为守护进程
        self.daemon = True
        self.listener = listener
        self.port = port
        self.baudrate = baudrate

    def run(self):
        with serial.Serial(port=self.port, baudrate=self.baudrate, timeout=.5) as ser:
            while True:
                debug_pre, debug_head = None, None
                while debug_pre == None:
                    debug_pre = ser.read(1)
                if not debug_pre or debug_pre[0] != 0x11:
                    continue

                while debug_head == None:
                    debug_head = ser.read(1)
                if not debug_head:
                    continue
                # convert into two number
                # pdb.set_trace()
                debug_type, debug_data_len = map(lambda x: int(x, 16), debug_head.hex())
                # read debug data area
                debug_data = None
                debug_data = ser.read(debug_data_len)
                
                if not self.listener.have_type(debug_type): 
                    # 未知类型
                    continue
                    
                print("Type:", f"{debug_type}({self.listener.get_type_name(debug_type)})")
                handler = self.listener.get_handler(debug_type)
                if not handler:
                    # 找不到指定的handler
                    print("Warning: 找不到handler")

                if len(debug_data) != debug_data_len:
                    print("Error: 包解析错误", list(map(lambda x: hex(x)[2:].upper(), debug_data)))
                else:
                    # pdb.set_trace()
                    unpack_str = self.listener.get_unpack_str(debug_type)
                    if unpack_str:
                        handler(struct.unpack(unpack_str, debug_data))
                    else:
                        handler(debug_data)
                print()

def list_ports():
    from winreg import OpenKey, EnumValue, QueryInfoKey, HKEY_LOCAL_MACHINE
    with OpenKey(HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\SERIALCOMM") as comm:
        count = QueryInfoKey(comm)[1]
        for i in range(count):
            name, value, _ = EnumValue(comm, i)
            print(name, value)