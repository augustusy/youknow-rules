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


def getList(listUrl):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', listUrl, timeout=10).data
    return data

def getGfwList():
    # the url of gfwlist
    baseurl = 'https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile = './list/tmp'

    gfwListTxt = codecs.open('./list/gfwlist.txt', 'w', 'utf-8')
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
                    gfwListTxt.write('DOMAIN-SUFFIX,%s,Proxy\n' % (domain[0]))
            else:
                continue

    tfs.close()
    gfwListTxt.close()

def getShadowrocketChinaIPList():
    # the url of chinaIP
    #baseurl = 'https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt'
    baseurl = 'https://gitlab.com/augustusy/omg/-/raw/master/china_ip_list.txt'

    try:

        content = getList(baseurl)
        content = content.decode('utf-8')
        f = codecs.open('./list/chinaIPlist', 'w', 'utf-8')
        f.write(content)
        f.close()
    except:
        print('Get IPlist update failed,use cache to update instead.')

    ipList = codecs.open('./list/chinaIPlist', 'r', 'utf-8')
    ipListTxt = codecs.open('./list/srchinaIPlist.txt', 'w', 'utf-8')
    ipListTxt.write('# chinaIP list updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    # Write list
    for line in ipList.readlines():

        ip = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', line)
        if len(ip) > 0:
            ipListTxt.write('IP-CIDR,%s,DIRECT\n' % (ip[0]))

    ipListTxt.close()
    ipListTxt.close()

def getPeterLowelist():
    # the url of Peter Lowe’s Ad and tracking server list​​​​​
    #baseurl = 'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext&_=4'
    baseurl = 'https://gitlab.com/augustusy/omg/-/raw/master/PeterLowe_Ad_and_tracking_server_list'

    comment_pattern = '^\#'
    domain_pattern = '^\d+\.\d+\.\d+\.\d+\s+([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    try:

        content = getList(baseurl)
        content = content.decode('utf-8')
        f = codecs.open('./list/PeterLowelist', 'w', 'utf-8')
        f.write(content)
        f.close()
    except:
        print('Get PeterLowelist update failed,use cache to update instead.')

    PLList = codecs.open('./list/PeterLowelist', 'r', 'utf-8')
    PLListTxt = codecs.open('./list/PeterLowelist.txt', 'w', 'utf-8')
    PLListTxt.write('# Peter Lowe’s Ad and tracking server list​​​​​ updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
	
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
                    PLListTxt.write('DOMAIN-SUFFIX,%s,REJECT\n' % (domainP[0]))
            else:
                continue

    PLListTxt.close()
    PLList.close()

#def getQuanChinaIPList():
    # the url of chinaIP
#    ipList = codecs.open('./list/chinaIPlist', 'r', 'utf-8')
#    ipListTxt = codecs.open('./list/QuanchinaIPlist.txt', 'w', 'utf-8')
#    ipListTxt.write('# chinaIP list updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" + '\n'))
    # Write list
#    for line in ipList.readlines():

#        ip = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', line)
#        if len(ip) > 0:
#            ipListTxt.write('IP-CIDR,%s,国内\n' % (ip[0]))

#    ipListTxt.close()
#    ipListTxt.close()

def genShadowrocketGFWAndChinaIPConf():
    f = codecs.open('template/sr_gfw&chinaIP_conf', 'r', 'utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r', 'utf-8')
    iplist = codecs.open('list/srchinaIPlist.txt', 'r', 'utf-8')
    pplist = codecs.open('list/PeterLowelist.txt', 'r', 'utf-8')
    file_content = f.read()
    iplist_buffer = iplist.read()
    gfwlist_buffer = gfwlist.read()
    pplist_buffer = pplist.read()
    pplist.close()
    gfwlist.close()
    iplist.close()
    f.close()

    GEOIPList = 'GEOIP,cn,DIRECT'
	
    file_content = file_content.replace('#__GFWLIST__#', gfwlist_buffer.replace('Proxy', 'PROXY'))
    file_content = file_content.replace('#__PeterLowelist__#', pplist_buffer)
    confs = codecs.open('configFileHere/ay_SR_nochinaIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

    file_content = file_content.replace('#__GEOIPList__#', GEOIPList)
    confw = codecs.open('configFileHere/ay_SR_gfw&GEOIP.conf', 'w', 'utf-8')
    confw.write(file_content)
    confw.close()

    file_content = file_content.replace(GEOIPList, '')
    file_content = file_content.replace('#__CHINAIP__#', iplist_buffer)
    confs = codecs.open('configFileHere/ay_SR_gfw&chinaIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

def genkitsunebiGFWAndChinaIPConf():
    f = codecs.open('template/kit_gfw&chinaIP_conf', 'r', 'utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r', 'utf-8')
    iplist = codecs.open('list/srchinaIPlist.txt', 'r', 'utf-8')
    pplist = codecs.open('list/PeterLowelist.txt', 'r', 'utf-8')
    file_content = f.read()
    iplist_buffer = iplist.read()
    gfwlist_buffer = gfwlist.read()
    pplist_buffer = pplist.read()
    pplist.close()
    gfwlist.close()
    iplist.close()
    f.close()

    GEOIPList = 'GEOIP,cn,DIRECT'

    file_content = file_content.replace('#__GFWLIST__#', gfwlist_buffer.replace('Proxy', 'PROXY'))
    file_content = file_content.replace('#__PeterLowelist__#', pplist_buffer)
    confs = codecs.open('configFileHere/ay_Kit_nochinaIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

    file_content = file_content.replace('#__GEOIPList__#', GEOIPList)
    confw = codecs.open('configFileHere/ay_Kit_gfw&GEOIP.conf', 'w', 'utf-8')
    confw.write(file_content)
    confw.close()

    file_content = file_content.replace(GEOIPList, '')
    file_content = file_content.replace('#__CHINAIP__#', iplist_buffer)
    confs = codecs.open('configFileHere/ay_Kit_gfw&chinaIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

def genQuantumultGFWAndChinaIPConf():
    f = codecs.open('template/quan_gfwlist&whiteIP_conf', 'r', 'utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r', 'utf-8')
    iplist = codecs.open('list/srchinaIPlist.txt', 'r', 'utf-8')
    pplist = codecs.open('list/PeterLowelist.txt', 'r', 'utf-8')
    file_content = f.read()
    iplist_buffer = iplist.read()
    gfwlist_buffer = gfwlist.read()
    pplist_buffer = pplist.read()
    pplist.close()
    gfwlist.close()
    iplist.close()
    f.close()

    GEOIPList = 'GEOIP,cn,DIRECT'

    file_content = file_content.replace('#__GFWLIST__#', gfwlist_buffer.replace('Proxy', 'PROXY'))
    file_content = file_content.replace('#__PeterLowelist__#', pplist_buffer)
    confs = codecs.open('configFileHere/ay_Quan_nochinaIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

    file_content = file_content.replace('#__GEOIPList__#', GEOIPList)
    confw = codecs.open('configFileHere/ay_Quan_gfw&GEOIP.conf', 'w', 'utf-8')
    confw.write(file_content)
    confw.close()

    file_content = file_content.replace(GEOIPList, '')
    file_content = file_content.replace('#__CHINAIP__#', iplist_buffer)
    confs = codecs.open('configFileHere/ay_Quan_gfw&chinaIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

def main():
    print('Getting GFW list...')
    getGfwList()
    print('Getting chinaIP list...')
    getShadowrocketChinaIPList()
    print('Getting PeterLowelist list...')
    getPeterLowelist()

    print('Generate config file...')	
    genShadowrocketGFWAndChinaIPConf()
    print('Generate config file:Shadowrocket conf files success')
    genkitsunebiGFWAndChinaIPConf()
    print('Generate config file:Kitsunebi conf files success')
    genQuantumultGFWAndChinaIPConf()
    print('Generate config file:Quantumult conf files success')
	
    print('All done!')
    print('Now you need edit config file to add your server infomation.')


if __name__ == '__main__':
    main()
