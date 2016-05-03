#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import re
import subprocess
import os
print os.getcwd()
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
def getDom(domainName):
    url = 'http://whois.chinaz.com/'+domainName
    cmd = "phantomjs %s %s"%(os.getcwd()+'\whois.js',url)
    print cmd
    stdout,stderr = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    return stdout
def getRegistry(Dom):
    htmlCharset = "GB2312"
    soup = BeautifulSoup(Dom,fromEncoding=htmlCharset)
    div = soup.findAll('div')
    registryInfo = dict()
    if div:
        for div_sub in div:
            for item in div_sub.contents:
                if isinstance(item,NavigableString):
                    item_str =  str(item.string).decode('utf-8','ignore')
                    # print len(item_str),item_str
                    index = item_str.find(':')
                    # print index
                    if index != -1:
                        key = item_str[:index].rstrip().lstrip()
                        if key in ['Domain Name','Registrar','Registrar WHOIS Server','更新时间','Registrar Registration 过期时间','Registrant City','Registrant Name','Registrant Organization','Registrant State/Province','Registrant Postal Code','Registrant Country','Registrant Phone','Registrant Email']:
                            # print 'in key list'
                            value = item_str[index+1:].rstrip().lstrip()
                            registryInfo[key] = value
                            # print key+':'+value
                        else:
                            pass
        return registryInfo
    else:
        print 'no url registry infomation'
        return None
if __name__ == '__main__':
    domainName = 'souhu.com'
    html_str = getDom(domainName)
    # print html_str
    registry_dict = getRegistry(html_str)
    # 输出返回的注册信息
    for key in registry_dict.keys():
        print key+':'+registry_dict[key]