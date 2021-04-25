# -*- coding: utf-8 -*-

#
# 参考并感谢：https://github.com/h2y/Shadowrocket-ADBlock-Rules/tree/master/factory
#
# 对于混合性质的网站，尽量走代理（忽略了所有的@@指令）
#

import os
import time
import sys
import requests
import re
import base64
import shutil


def get_rule(rules_url):
    rule = ''
    # 根据网络状况设置代理（pip install requests[socks]）
    my_proxy={"http":"socks5://127.0.0.1:7891","https":"socks5://127.0.0.1:7891"}
    for rule_url in rules_url:
        print('Loading: ' + rule_url)
        # 获取网页内容
        success = False
        try_times = 0
        r = None
        while try_times < 5 and not success:
            #r = requests.get(rule_url, proxies = my_proxy)
            r = requests.get(rule_url)
            if r.status_code != 200:
                time.sleep(1)
                try_times = try_times + 1
            else:
                success = True
                break

        if not success:
            sys.exit('error in request %s\n\treturn code: %d' % (rule_url, r.status_code) )

        rule = rule + r.text + '\n'

    return rule

def clear_format_for_GFW(rule):
    rules = []

    # 网页内容分割成行
    rule = rule.split('\n')

    for row in rule:
        row = row.strip()

        # 注释 直接跳过
        if row == '' or row.startswith('!') or row.startswith('@@') or row.startswith('[AutoProxy'):
            continue

        # 清除前缀
        row = re.sub(r'^\|?https?://', '', row)
        row = re.sub(r'^\|\|', '', row)
        row = row.lstrip('.*')

        # 清除后缀
        row = row.rstrip('/^*')

        rules.append(row)

    return rules

def clear_format_for_ADB(rule):
    # 包含域名和IP
    domains = []

    # 网页内容分割成行
    rule = rule.split('\n')

    for row in rule:
        row = row.strip()
        row0 = row

        ## 处理广告例外规则

        if row.startswith('@@'):
            i = 0
            while i < len(domains):
                domain = domains[i]
                if domain in row:
                    del domains[i]
                else:
                    i = i + 1

            continue

        ## 处理广告黑名单规则

        # 清除Peter Lowe’s规则前缀
        row = row.replace('127.0.0.1 ', '')

        # 直接跳过
        if row=='' or row.startswith('!') or "$" in row or "##" in row or row.startswith('#') :
            continue

        # 清除前缀
        row = re.sub(r'^\|?https?://', '', row)
        row = re.sub(r'^\|\|', '', row)
        row = row.lstrip('.*')

        # 清除后缀
        row = row.rstrip('/^*')
        row = re.sub(r':\d{2,5}$', '', row)  # 清除端口

        # 不能含有的字符
        if re.search(r'[/^:*]', row):
            #print('genADBlist >>> ignore: '+row0)
            continue

        # 只匹配域名或 IP
        if re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,9}$', row) or re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', row):
            domains.append(row)

    return domains

def filtrate_rules(rules):
    ret = []
    unhandle_rules = []

    for rule in rules:
        rule0 = rule

        # only hostname
        if '/' in rule:
            split_ret = rule.split('/')
            rule = split_ret[0]

        if not re.match('^[\w.-]+$', rule):
            unhandle_rules.append(rule0)
            continue

        ret.append(rule)

    ret = list( set(ret) )
    ret.sort()

    return ret, unhandle_rules

def getRulesStringFromed(row, kind):
    ret = ''
    content = row
    if len(content):
        if content.startswith('#'):
            return content
        else:
            prefix = 'HOST-SUFFIX'
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content):
                prefix = 'IP-CIDR'
                if '/' not in content:
                    content += '/32'
            elif '.' not in content:
                prefix = 'HOST-KEYWORD'

            ret += prefix + ',%s,%s' % (content, kind)

    return ret


def genGFWlist():

    rules_url = [
        # 选其中一个即可
        # Gitlab
        'https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt',
        # Github
        #'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt',	
	]

    ## 获取网页内容
    print('>>>>      Getting GFW list...       <<<<')
    rule = get_rule(rules_url)

    ## 解码
    rule = base64.b64decode(rule) \
            .decode("utf-8") \
            .replace('\\n', '\n')

    ## 清洗规则
    rules = clear_format_for_GFW(rule)
    print('Clear format done.')
	
    rules, unhandle_rules = filtrate_rules(rules)

    ## 写入文件（file_ad文件用于生成临时文件查错）

    # 输出详细执行日志
    #file_gfw = sys.stdout
    #file_gfwf = sys.stdout

    try:
        if sys.version_info.major == 3:
            file_gfw = open('tmp/GFWlist.tmp', 'w', encoding='utf-8')
            file_gfwf = open('Output/GFWlist.list', 'w', encoding='utf-8')
        else:
            file_gfw = open('tmp/GFWlist.tmp', 'w')
            file_gfwf = open('Output/GFWlist.list', 'w')
    except:
        pass

    file_gfw.write('# GFW rules refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')
    file_gfwf.write('# GFW rules refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')

    for row in rules:
        file_gfw.write(row + '\n')

        row = getRulesStringFromed(row, 'PROXY')
        file_gfwf.write(row + '\n')
    print('Rules String Fromed & File Writed.')

    file_gfw.close()
    file_gfwf.close()

    ## 复制到同步目录
    shutil.copy ('Output/GFWlist.list', '../../QuanX/Rules/Filter/GFWlist.list')


def genADBlist():

    rules_url = [
        # EasyList China
        #'https://easylist-downloads.adblockplus.org/easylistchina.txt',
        # EasyList + China
        'https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt',
        # 乘风 广告过滤规则
        'https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/ABP-FX.txt',
        # Peter Lowe’s Ad and tracking server list
        'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext&_=9',
        # uBlock-filters
        'https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt',
        # uBlock-filters Privacy
        'https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt',
    ]

    ## 获取网页内容
    print('>>>>       Getting ADB list...      <<<<')
    rule = get_rule(rules_url)

    ## 清洗规则
    domains = clear_format_for_ADB(rule)
    print('Clear format done.')

    ## 写入文件（file_ad文件用于生成临时文件查错）

    # 输出详细执行日志
    #file_ad = sys.stdout
    #file_adf = sys.stdout

    try:
        if sys.version_info.major == 3:
            file_ad = open('tmp/ADB.tmp', 'w', encoding='utf-8')
            file_adf = open('Output/ADB.list', 'w', encoding='utf-8')
        else:
            file_ad = open('tmp/ADB.tmp', 'w')
            file_adf = open('Output/ADB.list', 'w')
    except:
        pass

    file_ad.write('# adblock rules (EasyList + China + 乘风规则 + Peter Lowe’s规则+ uBlock-filters + uBlock-filters-Privacy) refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')
    file_adf.write('# adblock rules (EasyList + China + 乘风规则 + Peter Lowe’s规则+ uBlock-filters + uBlock-filters-Privacy) refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')

    # 去重复、转换成列表、排序
    domains = list( set(domains) )
    domains.sort()

    for item in domains:
        file_ad.write(item + '\n')

        item = getRulesStringFromed(item, 'REJECT')
        file_adf.write(item + '\n')
    print('Rules String Fromed & File Writed.')

    file_ad.close()
    file_adf.close()

    ## 复制到同步目录
    shutil.copy ('Output/ADB.list', '../../QuanX/Rules/Filter/ADB.list')

def genChinaIP():

    rules_url = ['https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt'
	]

    ## 获取网页内容
    print('>>>>    Getting ChinaIP list...     <<<<')
    ipList = get_rule(rules_url)

    ## 写入文件（file_ad文件用于生成临时文件查错）

    # 输出详细执行日志
    #file_gfw = sys.stdout
    #file_gfwf = sys.stdout

    try:
        if sys.version_info.major == 3:
            file_ip = open('tmp/ChinaIP.tmp', 'w', encoding='utf-8')
            file_ipf = open('Output/ChinaIP.list', 'w', encoding='utf-8')
        else:
            file_ip = open('tmp/ChinaIP.tmp', 'w')
            file_ipf = open('Output/ChinaIP.list', 'w')
    except:
        pass

    file_ip.write('# China IP list refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')
    file_ipf.write('# China IP list refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')

    # 网页内容分割成行
    ipList = ipList.split('\n')

    for row in ipList:
        row = row.strip()
        if len(row) > 0:
            file_ip.write(row + '\n')
            file_ipf.write('IP-CIDR,%s,DIRECT\n' % (row))

    print('Rules String Fromed & File Writed.')

    file_ip.close()
    file_ipf.close()

    ## 复制到同步目录
    shutil.copy ('Output/ChinaIP.list', '../../QuanX/Rules/Filter/ChinaIP.list')


# 主函数
def main():

    path = os.getcwd()
    path1 = path + '\\' + 'tmp'
    path2 = path + '\\' + 'Output'
    if not os.path.exists(path1):
        os.makedirs(path1)
    if not os.path.exists(path2):
        os.makedirs(path2)

    genGFWlist()
    print('>>>>   GFW list Generate success!   <<<<')
    print('========================================')

    genADBlist()
    print('>>>>   ADB list Generate success!   <<<<')
    print('========================================')

    genChinaIP()
    print('>>>> ChinaIP list Generate success! <<<<')
    print('========================================')

    print('All done!')
    print('Now you need edit these files to sure they are right.')


if __name__ == '__main__':
    main()




