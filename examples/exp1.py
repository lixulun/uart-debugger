
import sys, os
sys.path.append("..")

import pdb
from uart_debugger import TypeDefine, TypeHandler, UartListener, UartDebugger

class TypeOneHandler(TypeHandler):

    # https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment
    _unpack_str = ">H"

    def __call__(self, data):
        super().__call__(data)
        print(list(data))


listener = UartListener()
listener.register(TypeDefine(1, "type1", TypeOneHandler()))

# 参数和具体环境有关
uart_debugger = UartDebugger(listener, port="COM4", baudrate=19200)
uart_debugger.start()

# 主线程等待
uart_debugger.join()