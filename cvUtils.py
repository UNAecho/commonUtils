import random
import time

import cv2 as opencv
import numpy as np
from PIL import ImageGrab
from repository import templateEntity


window_info_tuple = None

if __name__ != 'main':
    template_cv2_entity = templateEntity.generate_all_template_gray_ndarray_of_cv2()


# threshold : 阈值，越接近1，匹配度要求越高。
# custom_coordinate : 自定义偏移量，用于自行修正坐标偏移量。
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
            result_coordinates['x'] = gps[0] + random.randint(10, 20)
            result_coordinates['y'] = gps[1] + random.randint(5, 10)
    except UnboundLocalError:
        print("寻找模板出错了，推测为没找到，想要找的模板为： " + template_file_name)
        result_coordinates = {}

    return result_coordinates


# 该方法返回多个模板的坐标
def multi_template_coordinate(template_file_name, threshold, custom_coordinate=None):

    # 返回找到的坐标值元组，调用方需要根据返回的字典进行拆包，得到坐标
    result_list = []
    # 读取cv2所使用的BGR模板
    template_imread = template_cv2_entity[template_file_name]
    if custom_coordinate is None:
        screen = np.array(ImageGrab.grab(window_info_tuple))
    else:
        custom_locale = (window_info_tuple[0] + custom_coordinate[0],
                         window_info_tuple[1] + custom_coordinate[1],
                         window_info_tuple[2] + custom_coordinate[2],
                         window_info_tuple[3] + custom_coordinate[3]
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
            coordinates_x = gps[0] + random.randint(5, 10) + window_info_dict['window_x_left']
            coordinates_y = gps[1] + random.randint(5, 10) + window_info_dict['window_y_top']
            result_list.append((coordinates_x, coordinates_y))
    except UnboundLocalError:
        print("寻找模板出错了，推测为没找到，想要找的模板为： " + template_file_name)
        result_list = []

    return result_list