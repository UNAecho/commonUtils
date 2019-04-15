import random
import time

import cv2 as opencv
import numpy as np
from PIL import ImageGrab
from repository import templateEntity

if __name__ == 'main':
    template_cv2_entity = templateEntity.generate_all_template_gray_ndarray_of_cv2()


# threshold:阈值，越接近1，匹配度要求越高。
def identify_find_template_or_not(template_file_name, threshold, custom_coordinate=None):

    # 返回找到的坐标值，调用方需要根据返回值点击
    result_coordinates = {}
    # 读取cv2所使用的BGR模板
    template_imread = template_cv2_entity[template_file_name]
    if custom_coordinate is None:
        screen = np.array(ImageGrab.grab(window_info_tuple))
    else:
        custom_locale = (window_info_tuple[0]+custom_coordinate[0],
                         window_info_tuple[1]+custom_coordinate[1],
                         window_info_tuple[2]+custom_coordinate[2],
                         window_info_tuple[3]+custom_coordinate[3]
                         )
        screen = np.array(ImageGrab.grab(custom_locale))
    img_bgr = opencv.cvtColor(screen, opencv.COLOR_RGB2BGR)
    gray_img_for_cv2 = opencv.cvtColor(img_bgr, opencv.COLOR_BGR2GRAY)

    match_res = opencv.matchTemplate(gray_img_for_cv2, template_imread, opencv.TM_CCOEFF_NORMED)

    try:
        loc = np.where(match_res >= threshold)
        for pt in zip(*loc[::-1]):
            gps = pt
        # loc中为匹配处左上角位置，正常会加一点点偏移量以保证点到图片中间
            result_coordinates['x'] = gps[0] + random.randint(5, 20) + window_info_dict['window_x_left']
            result_coordinates['y'] = gps[1] + random.randint(5, 20) + window_info_dict['window_y_top']
    except UnboundLocalError:
        print("寻找模板出错了，推测为没找到，想要找的模板为： " + template_file_name)
        result_coordinates = {}

    return result_coordinates