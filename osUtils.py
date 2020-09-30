import os
import operation
from time import sleep
import sys


# type :reset,shutdown,sleep
def shutdown_computer(self, type):
    sleep(1)
    operation.wait_to_click("start_button.png")
    sleep(1)
    operation.wait_to_click("shutdown.png")
    sleep(1)
    if type == "reset":
        operation.wait_to_click("reset.png")
    elif type == "shutdown":
        operation.wait_to_click("shutdown.png")
    else:
        operation.wait_to_click("sleep.png")


# 判断程序是不是在debug模式下运行
def is_debug():
    # sys.py 源码： gettrace() -- get the global debug tracing function
    # 用这种方法来判断当前py代码是不是在debug下运行，是则true，否则false
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is None:
        return False
    elif gettrace():
        return True
    else:
        return False
