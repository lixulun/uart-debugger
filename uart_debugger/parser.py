from collections import deque

class Parser:

    def __init__(self, serial):
        """
        serial serial.Serial实例
        """
        self._serial = serial
        self._raw_data = []

    def eat_all(self):
        """
        读取所有缓冲数据
        """
        self._raw_data.append(self._serial.read(self._serial.in_waiting))

    def parse(self):
        raw_data = b''.join(self._raw_data)
        i = 0
        while i < len(raw_data):
            if raw_data[i] == 0x11:

                # 最后一个字节是起始位，放到下一次处理
                if i+1 >= len(raw_data):
                    break

                data_type, data_len = raw_data[i+1]>>4, raw_data[i+1]&0x0F
                # 数据包不完整，放到下一次处理
                if i+data_len+1 >= len(raw_data):
                    break

                yield data_type, raw_data[i+2:i+2+data_len]
                i+=data_len+2
            else:
                i+=1
        self._raw_data.clear()
        if i < len(raw_data):
            self._raw_data.append(raw_data[i:])