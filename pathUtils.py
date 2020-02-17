import sys
from osUtils import is_debug


def get_project_dir():
    # 获取当前运行文件所在Project路径,sys.path中index包含各级路径，具体可以debug查看
    # !!!注意，debug和run分别是不同的执行文件，这将导致sys.path的value顺序会不同
    # 所以需要先判断是run还是debug，再进行工程dir的获取
    if is_debug():
        project_dir = sys.path[2]
    else:
        project_dir = sys.path[1]
    print("project_dir:" + project_dir)
    return project_dir
