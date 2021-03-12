import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from windowUtils import set_foreground_window
from operation import template_click as tc
from time import sleep
from cvUtils import identify_find_template_or_not
set_foreground_window("逍遥")


def get_rock():
    while True:
        if not identify_find_template_or_not("start_team_esit.png"):
            print("没发现开始战斗按钮，程序结束")
            continue
        tc("start_team_esit.png")
        sleep(5)
        if identify_find_template_or_not("clear.png"):
            print("没有体力了，看一下有没有要过期的药，吃了")
            if identify_find_template_or_not("overtime_hours.png"):
                print("有要过期的药，吃了")
                tc("confirm.png")
                sleep(3)
            else:
                print("没有即将过期的体力药，结束程序")
                break
        # 如果吃了药，就要再点一次开始战斗
        if identify_find_template_or_not("start_team_esit.png"):
            tc("start_team_esit.png")
        sleep(3.5)
        # 进入游戏战斗画面
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
            if identify_find_template_or_not("level_up3.png"):
                print("升级了！")
                sleep(2)
                tc("level_up.png")
            sleep(1)
        print("一轮战斗迭代结束")
        sleep(5)
get_rock()
print("任务完成，程序结束")
