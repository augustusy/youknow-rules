#!/usr/bin/env python3
# coding=utf-8
#
# 感谢dalao
# https://www.logcg.com

import urllib3
import re
import datetime
import certifi
import codecs
import shutil
import os
import os.path

def getList(listUrl):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', listUrl, timeout=10).data
    return data

def getandgenuasylistwithCN():
    # 把tmp文件夹下“easylist+CN.tmp”改名为“easylist2.tmp”(原文件备份)
    # 把Filter文件夹下“ADB+.list”复制到tmp文件夹，改名为“easylistCN2.tmp”(原文件备份)
    # 对新的“easylistCN2.tmp”内容进行处理（查重内容的“HOST-SUFFIX,”全部替换“||”，“,REJECT”全部删除）
    # 填入要合并的文件夹名字

    filedir = 'tmp/tmp'  # 填入要合并的文件夹名字
    if not os.path.exists(filedir): # 如果没有文件夹则创建
        os.makedirs(filedir)

    shutil.copy ('tmp/easylist2.tmp', 'tmp/tmp/easylist2.tmp')
    shutil.copy ('tmp/easylistCN2.tmp', 'tmp/tmp/easylistCN2.tmp')

    filenames = os.listdir(filedir)  # 获取文件夹内每个文件的名字
    f = open('tmp/easylistchachong.tmp', 'w')  # 以写的方式打开文件，没有则创建

    # 对文件夹内每个文件进行遍历
    for filename in filenames:
        filepath = filedir + '/' + filename  # 将文件夹路径和文件名字合并
        for line in open(filepath):  # 循环遍历对每一个文件内的数据
            f.writelines(line)  # 将数据每次按行写入f打开的文件中

    f.close()  # 关闭
    #print('easylist+easylistCN tmpfile Done!')

    comment_pattern = '^\!|\[|^@@|^\.|^\,|^\-|^\_|^\=|^\:|^\/|^\&|^\?|^\~|^\|\w|^\w|^\d+\.\d+\.\d+\.\d+|^\|\|\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    easylistTxt = codecs.open('./tmp/easylistchachong.txt', 'w', 'utf-8')
    easylistTxt.write('\n')

    tmpfile = './tmp/easylistchachong.tmp'

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
                except ValueError:
                    domainList.append(domain[0])
                    easylistTxt.write('HOST-SUFFIX,%s,REJECT\n' % (domain[0]))
            else:
                continue

    tfs.close()
    easylistTxt.close()
    shutil.rmtree("tmp/tmp")
    os.remove("tmp/easylistchachong.tmp")


def main():
    print('Getting easylist+easylistCN...')
    getandgenuasylistwithCN()
    print('Generate easylist+easylistCN success!')

    print('All done!')
    print('Now you need edit these files to sure they are right.')


if __name__ == '__main__':
    main()
