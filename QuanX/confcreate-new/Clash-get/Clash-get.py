# -*- coding: utf-8 -*-

#
# 作者：ysjlion
# 日期：20210311
# 备注：Gitlab有些地区被墙，尽量走代理。geoip离线库放在与该py文件同一目录下
#

import os
import time
import sys
import requests
import re
import shutil
import geoip2.database
# pip install geoip2 离线文件下载：https://dev.maxmind.com/geoip/geoip2/geolite2/
# pip install requests[socks]

def get_server(servers_url):
    server = ''
    # 根据网络状况设置代理
    my_proxy={"http":"socks5://127.0.0.1:7891","https":"socks5://127.0.0.1:7891"}
    for server_url in servers_url:
        print('Loading: ' + server_url)
        # 获取网页内容
        success = False
        try_times = 0
        r = None
        while try_times < 5 and not success:
            #r = requests.get(server_url, proxies = my_proxy)
            r = requests.get(server_url)
            if r.status_code != 200:
                time.sleep(1)
                try_times = try_times + 1
            else:
                success = True
                break

        if not success:
            sys.exit('error in request %s\n\treturn code: %d' % (server_url, r.status_code) )

        server = server + r.text + '\n'

    return server

def genClash():

    servers_url = [
        'https://gitlab.com/free9999/ipupdate/-/raw/master/clash/config.yaml',
        'https://gitlab.com/free9999/ipupdate/-/raw/master/clash/2/config.yaml',
        'https://gitlab.com/free9999/ipupdate/-/raw/master/clash/3/config.yaml',
	]

    ## 获取网页内容
    print('>>>>       Getting Clash servers list...      <<<<')
    servers = get_server(servers_url)

    ## 清洗
    #points = re.findall(r'(?<=\{)[^}]*(?=\})', str(servers))
    points = re.findall(r'(?<=\{).*(?=\})', str(servers))

    try:
        if sys.version_info.major == 3:
            file_points = open('Output/servers.tmp', 'w', encoding='utf-8')
            file_pointsfs = open('Output/ss-clash.txt', 'w', encoding='utf-8')
            file_pointsfv = open('Output/vmess-clash.txt', 'w', encoding='utf-8')			
        else:
            file_points = open('Output/servers.tmp', 'w')
            file_pointsfs = open('Output/ss-clash.txt', 'w')
            file_pointsfv = open('Output/vmess-clash.txt', 'w')
    except:
        pass

    file_points.write('# Clash Servers tempfile refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n\n')

    # 去重复、转换成列表
    points = list(set(points))

    pointsss = []
    pointsvm = []

    i = 10
    j = 10
    for row in points:
        row = row.strip()
        if len(row) > 0:
            file_points.write(row + '\n')
            if "type: ss" in row and "aes-256-gcm" in row:   
                row = re.sub(r'(\bname.*server\b): ','shadowsocks=',row)
                row = re.sub(', port: ',':',row)
                row = re.sub(', type: ss','',row)
                row = re.sub(', cipher: ',', method=',row)
                row = re.sub('password: ','password=',row)

                ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', row)
                ip = ip.group(0)
                #print (ip)
                reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
                response = reader.country(ip)
                #ipadd = response.country.iso_code
                ipadd = response.country.names['zh-CN']
                #print (ipadd)
                row = row + ', fast-open=false, udp-relay=false, tag=SS-' + str(i) + '(no-tls)' + str(ipadd)
                pointsss.append(row)
				
                i += 1

            if "type: vmess" in row and "port: 443" in row:   
                row = re.sub(r'(\bname.*server\b): ','vmess=',row)
                row = re.sub(', port: ',':',row)
                row = re.sub(', type: vmess','',row)
                row = re.sub(', uuid: ',', password=',row)
                row = re.sub(r', alterId: ([0-9]+)','',row)
                row = re.sub(', cipher: auto','',row)
                row = re.sub(', tls: true','',row)
                row = re.sub(', network: ws','',row)
                row = re.sub(', ws-path: ',', obfs-uri=',row)
                row = re.sub(', ws-headers: {Host: ',', obfs-host=',row)
                row = re.sub('}','',row)

                row = row + ', method=aes-128-gcm, tls13=true, obfs=wss, fast-open=false, udp-relay=false, tag=VM-' + str(j) + '(wss)德国'
                pointsvm.append(row)

                j += 1

    # 排序
    pointsss.sort()
    pointsvm.sort()

    # 写入
    i = i-10
    j = j-10
    file_pointsfs.write('# Clash SS Servers refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") + '  |  Servers Number：' + str(i) + '\n\n')
    file_pointsfv.write('# Clash Vmess Servers refresh time: ' + time.strftime("%Y-%m-%d %H:%M:%S") +  '  |  Servers Number：' + str(j) + '\n\n')
    for row1 in pointsss:
        file_pointsfs.write(row1 + '\n')
    for row2 in pointsvm:
        file_pointsfv.write(row2 + '\n')

    print('Servers Fromed & File Writed.')

    file_points.close()
    file_pointsfs.close()
    file_pointsfv.close()

    ## 复制到同步目录
    shutil.copy ('Output/ss-clash.txt', '../../sub/ss.txt')
    shutil.copy ('Output/vmess-clash.txt', '../../sub/vmess.txt')


# 主函数
def main():

    path = os.getcwd()
#    path1 = path + '\\' + 'tmp'
    path2 = path + '\\' + 'Output'
#    if not os.path.exists(path1):
#        os.makedirs(path1)
    if not os.path.exists(path2):
        os.makedirs(path2)

    genClash()

    print('All done!')
    print('Now you need edit these files to sure they are right.')


if __name__ == '__main__':
    main()




