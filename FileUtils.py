import os


def del_file_from_dir(path):
    # 列出该目录下的所有文件名
    filelist = os.listdir(path)
    for f in filelist:
        # 将文件名映射成绝对路径
        filepath = os.path.join(path, f)
        os.remove(filepath)
    print(path + "文件夹删除完毕")
