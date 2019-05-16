import win32api
from operation import mouse_click
import CVUtils
from time import sleep
from repository import templateEntity

if __name__ == 'main':
    template_cv2_entity = templateEntity.generate_all_template_gray_ndarray_of_cv2()

# print(win32api.GetCursorPos())
sleep(1)
for i in range(10):
    sleep(1)
    mouse_click(267,145)
    sleep(0.3)
    mouse_click(534,150)
    sleep(0.3)
    mouse_click(548,690)
    sleep(1.5)