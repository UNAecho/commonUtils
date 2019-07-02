from cvUtils import identify_find_template_or_not
from time import sleep
from operation import mouse_click
from operation import mouse_move
from operation import scroll_down
import keyboard_event

index_xy = identify_find_template_or_not(r"NewITIndex.png", 0.8)


def main_new_it():
    # 等待页面loading
    while not identify_find_template_or_not(r"NewITShare.png", 0.8):
        print("等待进入页面")
        sleep(1)
    while True:
        complete_xy = identify_find_template_or_not(r"NewITMarkascomplete.png", 0.8)

        if complete_xy:
            mouse_click(complete_xy['x'], complete_xy['y'])

        if identify_find_template_or_not(r"NewITBottomOfPage.png", 0.8):
            if identify_find_template_or_not(r"NewITLoading.png", 0.7):
                print("等待读取剩余页面信息")
                while not identify_find_template_or_not(r"NewITBottomOfPage.png", 0.8):
                    break
                continue
            else:
                print("做完该任务了，退出界面")
                mouse_click(index_xy['x'], index_xy['y'])
                keyboard_event.key_input("F5")
                while True:
                    if not identify_find_template_or_not(r"NewITWaitF5.png", 0.8):
                        print("按完F5等待刷新")
                    else:
                        break
                while True:
                    if identify_find_template_or_not(r"NewITWaitF5.png", 0.8):
                        print("刷新完毕")
                        sleep(2)
                        break
                    else:
                        print("没看到TOP按钮，判定正在刷新中，继续等待")

                return
        close_xy = identify_find_template_or_not(r"NewITClose.png", 0.8)
        if close_xy:
            mouse_click(close_xy['x'], close_xy['y'])
        scroll_down()
        sleep(0.5)


while True:
    sleep(0.5)
    if not identify_find_template_or_not(r"NewITWaitF5.png", 0.8):
        print("等待主页F5刷新")
        continue
    start_xy = identify_find_template_or_not(r"NewITClickToStart.png", 0.8)
    resume_xy = identify_find_template_or_not(r"NewITResume.png", 0.8)

    if start_xy:
        print("发现没开始的课程，进入开始做题")
        mouse_click(start_xy['x'], start_xy['y'])
        # 防止点的时候画面滚动，造成失效，再次点击找到的坐标
        if identify_find_template_or_not(r"NewITClickToStart.png", 0.8):
            mouse_click(start_xy['x'], start_xy['y'])
        main_new_it()
        continue
    elif resume_xy:
        print("发现没做了一半的课程，进入补全")
        mouse_click(resume_xy['x'], resume_xy['y'])
        # 防止点的时候画面滚动，造成失效，再次点击找到的坐标
        if identify_find_template_or_not(r"NewITResume.png", 0.8):
            mouse_click(resume_xy['x'], resume_xy['y'])
        main_new_it()
        continue
    else:
        print("没发现可以进入的课程，往下找")
        top_button_xy = identify_find_template_or_not(r"NewITWaitF5.png", 0.8)
        if top_button_xy:
            mouse_move(top_button_xy['x'], top_button_xy['y'])
        scroll_down()
        continue
