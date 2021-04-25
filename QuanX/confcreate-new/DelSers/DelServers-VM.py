# -*- coding: utf-8 -*-

#
# 作者：ysjlion
# 日期：20210318
#
# 【执行前先修改keyword】
#

import os

# keywords = ['key1', 'key2']
keywords = ['美国']

orgfile = '../../sub/vmess.txt'
bakfile = '../../sub/vmess.backup.txt'

try:
    os.rename(orgfile,bakfile)
    print('Rename vmess servers file success\r\n')
    with open(bakfile, 'r', encoding='utf-8') as oldfile, open(orgfile, 'w', encoding='utf-8') as newfile:
        for line in oldfile:
            if not any(keyword in line for keyword in keywords):
                newfile.write(line)
except Exception as e:
    print(e)
    print('Rename vmess servers file fail !\r\n')
else:
    print('All Done.')
