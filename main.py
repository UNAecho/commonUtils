import time
import windowUtils
import inputUtils
time.sleep(1)
windowUtils.set_foreground_window('MobaXterm')
time.sleep(1)
inputUtils.input_with_txt_end_with_enter(r"C:\study\test.txt")
