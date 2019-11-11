from setuptools import setup

setup(
    name="uart-debugger",
    version="0.0.3",
    packages=['uart_debugger'],
    install_requires=["pyserial"],
    test_suite="tests",
    author="Li Xulun",
    author_email="lixulun99@hotmail.com",
    description="自定义串口调试协议解析",
    license="MIT"
)