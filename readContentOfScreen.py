import pytesseract
from PIL import ImageGrab
import shutil
from datetime import datetime
from screenshot import getScreenshot

# 读取截图中的数字，多数用于各种挑战的数量剩余
# params:
# file_path:识别图片的路径
# screenshot_x:被截图左上角那一点的x轴坐标
# screenshot_y:被截图左上角那一点的y轴坐标
# screenshot_wight_x:图片x轴长度
# screenshot_high_y:图片y轴长度


def read_number_of_screen(screenshot_x_left, screenshot_y_upper, screenshot_x_right, screenshot_y_bottom):
    try:
        # 截屏，图片直接加入内存中,并使用.convert('L')处理为灰度图。
        # point规定除了255白色的像素点，都专为纯黑色0像素，而其它任何颜色，都转为255白色。
        # 理由是想做成白纸黑字的形式，便于OCR读取。
        # lambda是隐式函数的写法，具体网上可以搜到用法。
        im = ImageGrab.grab((screenshot_x_left, screenshot_y_upper, screenshot_x_right, screenshot_y_bottom)).convert('L').point(lambda x:0 if x ==255 else 255)
        read_screen_text = pytesseract.image_to_string(im)
        if read_screen_text is None or "":
            print("没读出来，这程序写的什么破玩意")
        return read_screen_text
    except Exception as e:
        print("读取数字出错！错误信息：" + str(e))
        # 输出读取错误的图片，方便人工debug原因
        # 请定期清理文件，不然文件夹体积会越来越大
        # error_image_filepath = 'errorImage\\' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
        # shutil.copyfile(file_path, error_image_filepath)
        # print("读取出错的图片路径为：" + error_image_filepath+"，请定期清理，防止文件夹越来越大")
        return "0"


def read_chi_of_screen(file_path, screenshot_x, screenshot_y, screenshot_wight_x, screenshot_high_y):
    getScreenshot(file_path, screenshot_x,
                  screenshot_y, screenshot_wight_x, screenshot_high_y)
    read_screen_text = pytesseract.image_to_string(Image.open(file_path), lang='chi_sim')
    return read_screen_text
