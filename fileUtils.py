import os


def batch_modify_file_contents(input_file_dir):
    filelist = os.listdir(input_file_dir)  # 该文件夹下所有的文件（包括文件夹）
    i = 0
