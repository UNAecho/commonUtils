import time
import keyboard_event
import msvcrt
import windowUtils


def input_with_txt_end_with_enter(filepath):
    with open(filepath, 'r') as f:
        # 按行读取，/n分割,输入之后按回车结束
        for line in f.readlines():
            windowUtils.set_foreground_window('MobaXterm')
            keyboard_event.key_input(line.strip())
            keyboard_event.input_enter()
            time.sleep(0.5)
            msvcrt.getch()
