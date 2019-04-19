import os
import re
import time


# env:选择INT、PREPROD、PROD
def batch_modify_file_contents(input_file_dir, env):
    for root, dirs, files in os.walk(input_file_dir):
        for name in files:
            with open(os.path.join(root, name), 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.03)
                # 提取正文
                content = f_r.read()
                # 提取当前表名
                table_name = extract_sql_table_name_lower(content)
                # 检索是否已经指定了location，如是，则省略当前DDL操作，继续迭代
                if re.search('hdfs\:\/\/', content, re.M | re.I):
                    print(table_name + " Location exists")
                    continue
                # # 寻找COMMENT位置，re.search返回符合匹配结果左闭右开的索引位置。
                # comment_index = re.search('COMMENT(\s*)\'[\w\t\. ]*\'', content, re.M | re.I).span()

                # 寻找TBLPROPERTIES位置，re.search返回符合匹配结果左闭右开的索引位置。
                reg_for_tblproperties = re.search('TBLPROPERTIES', content, re.M | re.I)

                # 判定是否有没加压缩格式的DDL，如是，则在文末添加
                if reg_for_tblproperties:
                    tblproperties_index = reg_for_tblproperties.span()
                else:
                    tblproperties_index = [len(content)]
                    count_line = content.find('\n')
                    if count_line < 1:
                        content = content + ' ' + r"TBLPROPERTIES('orc.compress'='SNAPPY')"
                    else:
                        content = content + '\n ' + r"TBLPROPERTIES('orc.compress'='SNAPPY')"
                # 分割文章，用于在断点处插入Location。
                new_content = content_segmentation_and_splicing(content, tblproperties_index, table_name, env)
            with open(os.path.join(root, name), 'w+') as f_w:
                f_w.write(new_content)


def extract_sql_table_name_lower(str):
    # re.M：多行匹配
    # re.I：大小写不敏感
    search_obj = re.search('(\s*)CREATE(\s*)(EXTERNAL)?(\s*)TABLE(\s*)(IF NOT EXISTS)?(\s*)`?(internalaudit_insight_12938\.)?(\w*)`?', str, re.M | re.I)
    # 第9组为TABLE名字
    return search_obj.group(9).lower()


# 分割文章
def content_segmentation_and_splicing(content, tblproperties_index, table_name, env):
    # 注意python的字符串[]索引用法规则是左闭右开，为了保证原文完整，左半部分索引结尾要+1
    content_tmp1 = content[:tblproperties_index[0]]
    content_tmp2 = content[tblproperties_index[0] - 1:]
    address = get_location_address(table_name, env)
    # 判断DDL是否是单行，如是，则拼接时不换行，特殊处理
    count_line = content.find('\n')
    if count_line < 1:
        new_content = content_tmp1 + ' ' + address + content_tmp2
    else:
        new_content = content_tmp1 + '\n' + address + '\n' + content_tmp2
    return new_content


# env:选择INT、PREPROD、PROD
def get_location_address(table_name,env):
    if env == 'PREPROD':
        return 'LOCATION \'hdfs://cioprdha/data/insight/cio/intaudit.pp/'+table_name+'\''
    return 'LOCATION \'hdfs://ciodevha/data/insight/cio/internalaudit/'+table_name+'\''


# # 验证正则表达式的正确性
# def reg_test(path,test_str):
#     comment_index = re.search('COMMENT(\s*)\'[\w \t\.]*\'', test_str, re.M | re.I).span()
#     print(comment_index)

def text(input_file_dir):
    for root, dirs, files in os.walk(input_file_dir):
        for name in files:
            with open(os.path.join(root, name), 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.05)
                # 提取正文
                content = f_r.read()
                # 提取当前表名
                table_name = extract_sql_table_name_lower(content)
                print(table_name)


def replace_content_in_dir(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            with open(os.path.join(root, name), 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.05)
                # 提取正文
                content = f_r.read()
                if 'ciodevha/data/insight/cio/internalaudit' in content:
                    new_content = content.replace('ciodevha/data/insight/cio/internalaudit','cioprdha/data/insight/cio/intaudit.pp')
                else:
                    print(name)
                    raise Exception
            with open(os.path.join(root, name), 'w') as f_w:
                f_w.write(new_content)
