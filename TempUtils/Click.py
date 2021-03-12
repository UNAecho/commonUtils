import sys

sys.path.append(r"D:\PyCharm Workspace\commonUtils")
print(sys.path)

from operation import wait_input_and_click

while True:
    count = int(input("输入连续点击次数："))
    wait_input_and_click("q", "e", count)
