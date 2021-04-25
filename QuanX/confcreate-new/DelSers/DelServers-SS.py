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

orgfile = '../../sub/ss.txt'
bakfile = '../../sub/ss.backup.txt'

try:
    os.rename(orgfile,bakfile)
    print('Rename SS servers file success\r\n')
    with open(bakfile, 'r', encoding='utf-8') as oldfile, open(orgfile, 'w', encoding='utf-8') as newfile:
        for line in oldfile:
            if not any(keyword in line for keyword in keywords):
                newfile.write(line)
except Exception as e:
    print(e)
    print('Rename SS servers file fail !\r\n')
else:
    print('All Done.')
