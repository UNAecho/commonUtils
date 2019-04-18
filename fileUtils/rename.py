import os


# 批量移除文件名中的_ddl
def batch_rename_file(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            old_name = os.path.join(root, name)
            new_name = old_name.replace('_ddl', '')
            os.renames(old_name,new_name)
