#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

/* 设置是否开启调试模式 */
#define UART_DEBUG_DEBUG_MODE 1

/* 根据自己的运行环境设置基本类型的大小 */
#define _int 4
#define _long 8

/* 需要实现发送单个字节的函数 */
extern void Uart_send_byte(unsigned char byte);

unsigned char _size_of_type(char t);
void Uart_debug(unsigned char *buf, unsigned int len);

void uart_debug_send(unsigned int type, char arg_types[], ...)
{
    unsigned char *sent_array, *p;
    unsigned int size_of_args = 0;
    char *c = arg_types;
    va_list ap;

    // 类型不能大于15
#if UART_DEBUG_DEBUG_MODE
    assert(type < 16);
#endif

    while(*c != '\0')
    {
        size_of_args += _size_of_type(*c);
        c++;
    }
    // 仅支持15个数据字节
#if UART_DEBUG_DEBUG_MODE
    assert(size_of_args < 16);
#endif
    c = arg_types;

    sent_array = (unsigned char*)malloc(size_of_args + 1);
#if dUART_DEBUG_DEBUG_MODE
    memset(sent_array, 0, size_of_args + 1);
#endif
    if(!sent_array)
        return;

    va_start(ap, arg_types);
    p = sent_array+1;
    while(*c != '\0')
    {
        unsigned char size_of_type = _size_of_type(*c);
        if(size_of_type == _long)
        {
            *(unsigned long*)p = va_arg(ap, unsigned long);
        }
        else if (size_of_type == _int)
        {
            *(unsigned int*)p = va_arg(ap, unsigned int);
        }
        else
        {
            *p = va_arg(ap, unsigned char);
        }
        p += size_of_type;
        c++;
    }

    sent_array[0] = (type << 4) + size_of_args;
    Uart_debug(sent_array, size_of_args + 1);

    va_end(ap);
    free(sent_array);
}

unsigned char _size_of_type(char t)
{
    switch(t)
    {
        case 'c':
        case 'b':
            return 1;
            break;
        case 'h':
        case 'H':
            return _int;
            break;
        case 'i':
        case 'I':
            return _long;
            break;
    }
    return 0;
}

#if UART_DEBUG_DEBUG_MODE
void Uart_send_byte(unsigned char byte)
{
    printf("%d ", byte);
}
#endif

void Uart_debug(unsigned char *buf, unsigned int len)
{
    unsigned int i = 0;
    Uart_send_byte(0x11);
    for(;i<len;i++)
    {
         Uart_send_byte(buf[i]);
    }
#if UART_DEBUG_DEBUG_MODE
    printf("\n");
#endif
}
