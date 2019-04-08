import time
import keyboard_event


def input_with_txt_end_with_enter(filepath):
    with open(filepath, 'r') as f:
        # 按行读取，/n分割,输入之后按回车结束
        for line in f.readlines():
            keyboard_event.key_input(line.strip())
            keyboard_event.input_enter()
            time.sleep(3.5)
