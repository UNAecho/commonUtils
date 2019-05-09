import os
import re
import time


# env:选择INT、PREPROD、PROD
def batch_modify_file_contents(input_file_dir, env):
    for root, dirs, files in os.walk(input_file_dir,topdown=False):
        for name in files:
            with open(os.path.join(root, name), 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.03)
                # 提取正文
                content = f_r.read()
                print("current file :" + name, end='')
                # 正则提取create语句一系列动作
                search_obj = re.search("(\s*)CREATE(\s*)(EXTERNAL)?(\s*)TABLE(\s*)(IF NOT EXISTS)?(\s*)`?(\s*internalaudit_[_preod]*insight_12938\.)?(\w*)`?", content, re.M | re.I)
                if "internalaudit_preprod_insight_12938." in search_obj.group(8):
                    print(name +"：检测到internalaudit_preprod_insight_12938写法，将其替换为internalaudit_insight_12938")
                    content = content.replace(search_obj.group(8), "internalaudit_insight_12938.", count=1)
                if not search_obj.group(8):
                    print(name +"：没有写DB，开始修正")
                    content = insert_str_into_content_for_db(content,search_obj.span(9)[0], "internalaudit_insight_12938.")
                if not search_obj.group(3):
                    content = re.sub("(\s*)CREATE(\s*)(EXTERNAL)?(\s*)TABLE(\s*)","CREATE EXTERNAL TABLE ",content)
                # 提取当前表名
                table_name = search_obj.group(9).lower()
                # 寻找COMMENT位置，re.search返回符合匹配结果左闭右开的索引位置。
                try:
                    split_index = re.search('COMMENT(\s*)\'[\w\s\.]*\'', content, re.M | re.I).span()
                except:
                    raise Exception("没找到COMMENT ，终止程序，请手动确认COMMENT信息")
                if re.search("PARTITIONED(\s*)BY(\s*)\([`\s\w\. ]*\)", content, re.M | re.I):
                    split_index = re.search("PARTITIONED(\s*)BY(\s*)\([`\s\w\. ]*\)", content, re.M | re.I).span()
                # 检索是否已经指定了分隔符，如是，则不作分隔符声明
                if re.search("ROW(\s+)FORMAT(\s+)DELIMITED(\s+)FIELDS(\s+)TERMINATED(\s+)BY(\s*)\'\\\(\w)\'", content, re.M | re.I):
                    print(" ROW FORMAT DELIMITED FIELDS exists", end='')
                    split_index = re.search("ROW(\s+)FORMAT(\s+)DELIMITED(\s+)FIELDS(\s+)TERMINATED(\s+)BY(\s*)\'\\\(\w)\'", content, re.M | re.I).span()
                else:
                    content = insert_str_into_content(content, split_index[1], r"ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'")
                    split_index = re.search("ROW(\s+)FORMAT(\s+)DELIMITED(\s+)FIELDS(\s+)TERMINATED(\s+)BY(\s*)\'\\\(\w)\'", content, re.M | re.I).span()
                # 检索是否已经指定了STORED存储格式，如是，则不作存储格式添加
                if re.search("STORED(\s+)AS(\s+)(\w+)", content, re.M | re.I):
                    print(", stored exists", end='')
                    split_index = re.search("STORED(\s+)AS(\s+)(\w+)", content, re.M | re.I).span()
                else:
                    content = insert_str_into_content(content, split_index[1], r"STORED AS ORC")
                    split_index = re.search("STORED(\s+)AS(\s+)(\w+)", content, re.M | re.I).span()
                # 检索是否已经指定了location
                if re.search("\'hdfs\:[\w\/\.]*\'", content, re.M | re.I):
                    # 如果当前为PREPROD，那么原来写好的INT地址换为PREPROD的
                    if r"ciodevha/data/insight/cio/internalaudit" in content and env == "PREPROD":
                        content = content.replace(r"ciodevha/data/insight/cio/internalaudit",r"cioprdha/data/insight/cio/intaudit.pp")
                    print(", Location exists", end='')
                    split_index = re.search("\'hdfs\:[\w\/\.]*\'", content, re.M | re.I).span()
                else:
                    address = get_location_address(table_name,env)
                    content = insert_str_into_content(content, split_index[1], address)
                    split_index = re.search("\'hdfs\:[\w\/\.]*\'", content, re.M | re.I).span()
                # 判定是否有没加压缩格式的DDL，如是，则添加TBLPROPERTIES
                if re.search("TBLPROPERTIES(\s*)\([\'\"]orc.compress[\'\"]=[\'\"](\w*)[\'\"]\)", content, re.M | re.I):
                    print(", TBLPROPERTIES exists")
                else:
                    content = insert_str_into_content(content, split_index[1], r"TBLPROPERTIES('orc.compress'='SNAPPY')")
            if env == "INT":
                with open(os.path.join(root, name), 'w+') as f_w:
                    f_w.write(content)
            else:
                if r"preprod" in root:
                    with open(os.path.join(root, name), 'w+') as f_w:
                        f_w.write(content)
                else:
                    with open(os.path.join(root, "preprod\\" + name), 'w+') as f_w:
                        f_w.write(content)


def insert_str_into_content(content, split_index, str_to_insert):
    # 注意python的字符串[]索引用法规则是左闭右开
    content_tmp1 = content[:split_index]
    content_tmp2 = content[split_index:]
    # 判断文件是否是单行，如是，则进行适用单行的特殊插入处理
    count_line = content.count('\n')
    if count_line <= 1:
        content = content_tmp1 + ' ' + str_to_insert + content_tmp2
    else:
        content = content_tmp1 + '\n' + str_to_insert + content_tmp2
    return content


def insert_str_into_content_for_db(content, split_index, str_to_insert):
    # 注意python的字符串[]索引用法规则是左闭右开
    content_tmp1 = content[:split_index]
    content_tmp2 = content[split_index:]
    content = content_tmp1 + ' ' + str_to_insert + content_tmp2
    return content


# env:选择INT、PREPROD、PROD
def get_location_address(table_name,env):
    if env == 'PREPROD':
        return "LOCATION \'hdfs://cioprdha/data/insight/cio/intaudit.pp/"+ table_name + "\'"
    return "LOCATION \'hdfs://ciodevha/data/insight/cio/internalaudit/" + table_name + "\'"


# # 验证正则表达式的正确性
# def reg_test(test_str):
#     comment_index = re.search('ROW(\s+)FORMAT(\s+)DELIMITED(\s+)FIELDS(\s+)TERMINATED(\s+)BY(\s*)\'\\\t\'',test_str, re.M | re.I).span()
#     print(comment_index)

# 提取某个路径下DDL的表名
def extract_table_name_temp_function(input_file_dir):
    for root, dirs, files in os.walk(input_file_dir):
        for name in files:
            with open(os.path.join(root, name), 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.05)
                # 提取正文
                content = f_r.read()
                # 提取当前表名
                # 正则提取create语句一系列动作
                search_obj = re.search("(\s*)CREATE(\s*)(EXTERNAL)?(\s*)TABLE(\s*)(IF NOT EXISTS)?(\s*)`?(internalaudit_[_preod]*insight_12938\.)?(\w*)`?", content, re.M | re.I)
                # 提取当前表名
                table_name = search_obj.group(9).lower()
                print(table_name)


# 批量替换文中文本，大小写以源文件中的大小写为准
def replace_content_in_dir(path, old_str, new_str):
    # 出错计数
    error_count = 0
    not_found_count = 0
    for file in os.listdir(path):
        abs_path = os.path.abspath(path+"\\"+file)
        if os.path.isfile(abs_path):
            with open(abs_path, 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.05)
                # 提取正文
                content = f_r.read()
                if old_str in content:
                    new_content = content.replace(old_str, new_str)
                elif old_str.upper() in content:
                    new_content = content.replace(old_str.upper(), new_str.upper())
                elif old_str.lower() in content:
                    new_content = content.replace(old_str.lower(), new_str.lower())
                else:
                    not_found_count += 1
                    print("file:"+file+" does not have :" + old_str + ",count :" + str(not_found_count))
                    continue
            with open(abs_path, 'w') as f_w:
                f_w.write(new_content)
        else:
            error_count += 1
            print(file + " is not file,count :"+str(error_count))


# 将目录下的所有文件内容读取到一个文件当中
def read_content_to_single_file(path):
    total_content = ""
    for file in os.listdir(path):
        # 用输入目录加上文件名，拼成绝对目录
        abs_path = os.path.abspath(path + "\\" + file)
        if os.path.isfile(abs_path):
            with open(abs_path, 'r+') as f_r:
                # 加延迟，防止打印串位置
                time.sleep(0.05)
                # 提取正文
                content = f_r.read()
                # 每次分号结尾，并换行
                total_content = total_content + content + ";\n"
        else:
            print("file :" + file + "is not a file .")
    with open(r"C:\Users\andi.you\Desktop\pyoutput.txt",'w+') as f_w:
        f_w.write(total_content)