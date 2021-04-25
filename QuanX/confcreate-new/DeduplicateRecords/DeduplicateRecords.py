#!/usr/bin/env python3
# coding=utf-8
#

# 使用方法：
#
# 把要查重的文件放到'IN'文件夹下，文件顺序影响输出排序！
# Dup-Records.txt 为重复记录。
# Outtmp.txt 为去重复后的临时文件。
# Out.txt 为去重复后的输出结果。
#

import re
import os
import codecs

filedir = 'IN'  # 查重文件所在目录

filenames = os.listdir(filedir)  # 获取文件夹内每个文件的名字
f = codecs.open('Chachongtmp.tmp', 'w', 'utf-8')  # 以写的方式打开文件，没有则创建

# 对文件夹内每个文件进行遍历
for filename in filenames:
    print(filename)
    filepath = filedir + '/' + filename  # 将文件夹路径和文件名字合并
    for line in codecs.open(filepath, 'r', 'utf-8'):  # 循环遍历对每一个文件内的数据
        if line.startswith('#') or line.startswith('HOST-KEYWORD,'):
            continue
        else: 
            f.writelines(line)  # 将数据每次按行写入allhost列表中

f.close()
print('tempfile Done.')

comment_pattern = '^\#'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

chTxt = codecs.open('Out.txt', 'w', 'utf-8')
chTxtt = codecs.open('Outtmp.txt', 'w', 'utf-8')
chTxtcf = codecs.open('Dup-Records.txt', 'w', 'utf-8')

tmpfile = 'Chachongtmp.tmp'
tfs = codecs.open(tmpfile, 'r', 'utf-8')

# Store all domains, deduplicate records
domainList = []

# Write list
for line in tfs.readlines():

    if re.findall(comment_pattern, line):
        continue
    else:
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainList.index(domain[0])
                chTxtcf.write('HOST-SUFFIX,%s,REJECT\n' % (domain[0]))
            except ValueError:
                domainList.append(domain[0])
                chTxtt.write(domain[0] + '\n')
                chTxt.write('HOST-SUFFIX,%s,REJECT\n' % (domain[0]))
        else:
            continue

tfs.close()
chTxt.close()
chTxtcf.close()

print('All Done.')
