from windowUtils import set_foreground_window
from operation import template_click as tc
from time import sleep
from cvUtils import identify_find_template_or_not
set_foreground_window("明日方舟")


def get_rock():
    while True:
        if not identify_find_template_or_not("start_team_esit.png"):
            print("没发现开始战斗按钮，程序结束")
            break
        tc("start_team_esit.png")
        sleep(2.5)
        tc("fight.png")
        print("开始战斗")
        while True:
            if identify_find_template_or_not("auto.png"):
                print("进入战斗界面")
                break
            sleep(1)
        while True:
            if not identify_find_template_or_not("auto.png"):
                print("战斗结束")
                break
            sleep(1)
        while True:
            if identify_find_template_or_not("win.png"):
                sleep(3)
                tc("win.png")
                break
            sleep(1)
        print("一轮战斗迭代结束")
        sleep(5)
get_rock()
