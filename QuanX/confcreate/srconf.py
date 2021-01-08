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

def getandgenGfwList():
    # the url of gfwlist
    #baseurl = 'https://raw.fastgit.org/gfwlist/gfwlist/master/gfwlist.txt'
    baseurl = 'https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile = './tmp/gfwlist.tmp'

    gfwListTxt = codecs.open('./tmp/gfwlist.txt', 'w', 'utf-8')
    gfwListTxt.write('# gfwlist updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    gfwListTxt.write('\n')

    try:

        data = getList(baseurl)
        content = codecs.decode(data, 'base64_codec').decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('GFW list fetched, writing...')
    except:
        print('GFW list fetch failed, use tmp instead...')
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
                    gfwListTxt.write('HOST-SUFFIX,%s,PROXY\n' % (domain[0]))
            else:
                continue

    tfs.close()
    gfwListTxt.close()
	
    shutil.copy ('tmp/gfwlist.txt', 'Output/GFWlist.list')

def getandgenChinaIPList():
    # the url of chinaIP
    #baseurl = 'https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt'
    #baseurl = 'https://raw.fastgit.org/17mon/china_ip_list/master/china_ip_list.txt'
    #baseurl = 'https://gitlab.com/augustusy/omg/-/raw/master/Sources/ChinIP.txt'   
    baseurl = 'https://cdn.jsdelivr.net/gh/17mon/china_ip_list/china_ip_list.txt'
    #刷新jsdelivr缓存：https://purge.jsdelivr.net/gh/17mon/china_ip_list/china_ip_list.txt

    try:

        content = getList(baseurl)
        content = content.decode('utf-8')
        f = codecs.open('./tmp/chinaIPlist.tmp', 'w', 'utf-8')
        f.write(content)
        f.close()
        print('Get IPlist fetched, writing...')
    except:
        print('Get IPlist update failed,use cache instead.')

    ipList = codecs.open('./tmp/chinaIPlist.tmp', 'r', 'utf-8')
    ipListTxt = codecs.open('./tmp/chinaIPlist.txt', 'w', 'utf-8')
    ipListTxt.write('# chinaIP list updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    ipListTxt.write('\n')

    # Write list
    for line in ipList.readlines():

        ip = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', line)
        if len(ip) > 0:
            ipListTxt.write('IP-CIDR,%s,DIRECT\n' % (ip[0]))

    ipListTxt.close()
    ipList.close()

    shutil.copy ('tmp/chinaIPlist.txt', 'Output/ChinaIP.list')

def getandgenPeterLowelist():
    # the url of Peter Lowe’s Ad and tracking server list​​​​​
    baseurl = 'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext&_=9'
    #baseurl = 'https://gitlab.com/augustusy/youknow-rules/-/raw/master/QuanX/confcreate/Sources/PeterLowe.txt'
    #baseurl = 'https://raw.fastgit.org/augustusy/youknow-rules/master/QuanX/confcreate/Sources/PeterLowe.txt'
    #baseurl = 'https://cdn.jsdelivr.net/gh/augustusy/youknow-rules/QuanX/confcreate/Sources/PeterLowe.txt'

    comment_pattern = '^\#'
    domain_pattern = '^\d+\.\d+\.\d+\.\d+\s+([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    try:

        content = getList(baseurl)
        content = content.decode('utf-8')
        f = codecs.open('./tmp/PeterLowelist.tmp', 'w', 'utf-8')
        f.write(content)
        f.close()
        print('Get PeterLowelist fetched, writing...')
    except:
        print('Get PeterLowelist update failed,use cache instead.')

    PLList = codecs.open('./tmp/PeterLowelist.tmp', 'r', 'utf-8')
    PLListTxt = codecs.open('./tmp/PeterLowelist.txt', 'w', 'utf-8')
    PLListTxt.write('# Peter Lowe’s Ad and tracking server list​​​​​ updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    PLListTxt.write('\n')

    domainList = []
	
    # Write list
    for line in PLList.readlines():

        if re.findall(comment_pattern, line):
            continue
        else:
            domainP = re.findall(domain_pattern, line)
            #print ("读取域名为: %s" % (domainP))
            if domainP:
                try:
                    found = domainList.index(domainP[0])
                except ValueError:
                    domainList.append(domainP[0])
                    PLListTxt.write('HOST-SUFFIX,%s,REJECT\n' % (domainP[0]))
            else:
                continue

    PLListTxt.close()
    PLList.close()

    shutil.copy ('tmp/PeterLowelist.txt', 'Output/ADB_PeterLowelist.list')

def getandgeneasylistCN():
    # the url of easylistCN
    baseurl = 'https://easylist-downloads.adblockplus.org/easylistchina.txt'

    comment_pattern = '^\!|\[|^@@|^\.|^\,|^\-|^\_|^\=|^\:|^\/|^\&|^\?|^\~|^\|\w|^\d+\.\d+\.\d+\.\d+|^\|\|\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile1 = './tmp/easylistCN1.tmp'
    tmpfile2 = './tmp/easylistCN2.tmp'

    easylistTxt = codecs.open('./tmp/easylistCN.txt', 'w', 'utf-8')
    easylistTxt.write('# easylistCN updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    easylistTxt.write('\n')

    try:

        data = getList(baseurl)
        content = data.decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile1, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('easylistCN fetched, writing...')
    except:
        print('easylistCN fetch failed, use tmp instead...')

    tmpf1 = codecs.open(tmpfile1, 'r', 'utf-8')
    tmpf2 = codecs.open(tmpfile2, 'w', 'utf-8')
    for line in tmpf1.readlines():
        if ("$" in line) or ("#" in line) or ("*" in line) or ("/" in line) or ("?" in line): #如果包含特殊字符就跳过
            continue
        line = line.replace('^','')	
        tmpf2.write(line)
    print('easylistCN filtered...')
    tmpf2.close
    tmpf1.close


    tfs = codecs.open(tmpfile2, 'r', 'utf-8')

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

    shutil.copy ('tmp/easylistCN.txt', 'Output/ADB_easylistCN.list')

def getandgeneasylist():
    # the url of easylist
    #baseurl = 'https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_adservers.txt'
    baseurl = 'https://easylist-downloads.adblockplus.org/easylist.txt'
    #baseurl = 'https://cdn.jsdelivr.net/gh//easylist/easylist/easylist/easylist_adservers.txt'
    #刷新jsdelivr缓存：https://purge.jsdelivr.net/gh//easylist/easylist/easylist/easylist_adservers.txt

    comment_pattern = '^\!|\[|^@@|^\.|^\,|^\-|^\_|^\=|^\:|^\/|^\&|^\?|^\~|^\|\w|\|$|^\d+\.\d+\.\d+\.\d+|^\|\|\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile1 = './tmp/easylist1.tmp'
    tmpfile2 = './tmp/easylist2.tmp'

    easylistTxt = codecs.open('./tmp/easylist.txt', 'w', 'utf-8')
    easylistTxt.write('# easylist updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    easylistTxt.write('\n')

    try:

        data = getList(baseurl)
        content = data.decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile1, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('easylist fetched, writing...')
    except:
        print('easylist fetch failed, use tmp instead...')

    tmpf1 = codecs.open(tmpfile1, 'r', 'utf-8')
    tmpf2 = codecs.open(tmpfile2, 'w', 'utf-8')
    for line in tmpf1.readlines():
        if ("$" in line) or ("#" in line) or ("*" in line) or ("/" in line) or ("?" in line): #如果包含c就跳过
            continue
        line = line.replace('^','')	
        tmpf2.write(line)
    print('easylist filtered...')
    tmpf2.close
    tmpf1.close


    tfs = codecs.open(tmpfile2, 'r', 'utf-8')

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

    shutil.copy ('tmp/easylist.txt', 'Output/ADB_easylist.list')

def getandgenuasylistwithCN():
    filedir = 'tmp/tmp'  # 填入要合并的文件夹名字
    if not os.path.exists(filedir): # 如果没有文件夹则创建
        os.makedirs(filedir)

    shutil.copy ('tmp/easylist2.tmp', 'tmp/tmp/easylist2.tmp')
    shutil.copy ('tmp/easylistCN2.tmp', 'tmp/tmp/easylistCN2.tmp')

    filenames = os.listdir(filedir)  # 获取文件夹内每个文件的名字
    f = open('tmp/easylist+CN.tmp', 'w')  # 以写的方式打开文件，没有则创建

    # 对文件夹内每个文件进行遍历
    for filename in filenames:
        filepath = filedir + '/' + filename  # 将文件夹路径和文件名字合并
        for line in open(filepath):  # 循环遍历对每一个文件内的数据
            f.writelines(line)  # 将数据每次按行写入f打开的文件中

    f.close()  # 关闭
    #print('easylist+easylistCN tmpfile Done!')

    comment_pattern = '^\!|\[|^@@|^\.|^\,|^\-|^\_|^\=|^\:|^\/|^\&|^\?|^\~|^\|\w|^\w|^\d+\.\d+\.\d+\.\d+|^\|\|\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    easylistTxt = codecs.open('./tmp/easylist+CN.txt', 'w', 'utf-8')
    easylistTxt.write('# easylist + easylistCN updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    easylistTxt.write('\n')

    tmpfile = './tmp/easylist+CN.tmp'

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

    shutil.copy ('tmp/easylist+CN.txt', 'Output/ADB_easylist+CN.list')

def getandgenuBlockfilters():
    # the url of uBlock filters
    #baseurl = 'https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt'
    baseurl = 'https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssets/filters/filters.txt'
    #刷新jsdelivr缓存：https://purge.jsdelivr.net/gh/uBlockOrigin/uAssets/filters/filters.txt
	
    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+|^\|\|\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile1 = './tmp/uBlockfilters1.tmp'
    tmpfile2 = './tmp/uBlockfilters2.tmp'

    easylistTxt = codecs.open('./tmp/uBlockfilters.txt', 'w', 'utf-8')
    easylistTxt.write('# uBlock filters updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    easylistTxt.write('\n')

    try:

        data = getList(baseurl)
		
        content = data.decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile1, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('uBlock filters fetched, writing...')
    except:
        print('uBlock filters fetch failed, use tmp instead...')

    tmpf1 = codecs.open(tmpfile1, 'r', 'utf-8')
    tmpf2 = codecs.open(tmpfile2, 'w', 'utf-8')
    for line in tmpf1.readlines():
        if ("$" in line) or ("#" in line) or ("*" in line) or ("/" in line): #如果包含c就跳过
            continue
        line = line.replace('^','')	
        tmpf2.write(line)
    print('uBlock filters filtered...')
    tmpf2.close
    tmpf1.close


    tfs = codecs.open(tmpfile2, 'r', 'utf-8')

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

    shutil.copy ('tmp/uBlockfilters.txt', 'Output/ADB_uBlockfilters.list')


def main():
    print('Getting GFW list...')
    getandgenGfwList()
    print('Generate GfwList success!')

    print('Getting chinaIP list...')
    getandgenChinaIPList()
    print('Generate chinaIP list success!')

    print('Getting PeterLowe list list...')
    getandgenPeterLowelist()
    print('Generate PeterLowe list success!')

    print('Getting easylistCN...')
    getandgeneasylistCN()
    print('Generate easylistCN success!')

    print('Getting easylist...')
    getandgeneasylist()
    print('Generate easylist success!')

    print('Getting easylist+easylistCN...')
    getandgenuasylistwithCN()
    print('Generate easylist+easylistCN success!')

    print('Getting uBlock filters...')
    getandgenuBlockfilters()
    print('Generate uBlock filters success!')

    print('All done!')
    print('Now you need edit these files to sure they are right.')


if __name__ == '__main__':
    main()
