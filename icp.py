import time
import hashlib
import requests
import json
import random
import urllib3
import argparse
urllib3.disable_warnings()

rannum1 = random.randint(1,255)
rannum2 = random.randint(1,255)
rannum3 = random.randint(1,255)
ip = f"101.{rannum1}.{rannum2}.{rannum3}"
head = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://beian.miit.gov.cn/",
        "Referer": "https://beian.miit.gov.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "CLIENT-IP": ip,
        "X-FORWARDED-FOR": ip
}
def get_token():
    timeStamp = int(time.time())
    authKey = hashlib.md5(("testtest" + str(timeStamp)).encode()).hexdigest()
    tokenurl = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth"
    data = {
        "authKey": authKey,
        "timeStamp": timeStamp
    }
    res = requests.post(url=tokenurl,headers=head,data=data,verify=False)
    return json.loads(res.text)['params']['bussiness']

tokens = get_token()

def get_code():
    codeurl = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage"
    codehead = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://beian.miit.gov.cn/",
        "Referer": "https://beian.miit.gov.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "token": tokens
    }
    rescode = requests.post(url=codeurl,headers=codehead,verify=False)
    return json.loads(rescode.text)['params']['uuid']

def get_domain(name):
    url = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition"
    domainhead = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "uuid": get_code(),
        "token": tokens,
        "Origin": "https://beian.miit.gov.cn/",
        "Referer": "https://beian.miit.gov.cn/"
    }
    data = {
        "pageNum": "1",
        "pageSize": "100",
        "unitName": name
    }
    domains = requests.post(url=url,headers=domainhead,json=data,verify=False).text
    domain =  json.loads(domains)['params']['list']
    for i in domain:
        print(i['domain'])

def get_icp(name):
    url = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition"
    domainhead = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "uuid": get_code(),
        "token": tokens,
        "Origin": "https://beian.miit.gov.cn/",
        "Referer": "https://beian.miit.gov.cn/"
    }
    data = {
        "pageNum": "1",
        "pageSize": "100",
        "unitName": name
    }
    icps = requests.post(url=url, headers=domainhead, json=data, verify=False).text
    domain = json.loads(icps)['params']['list']
    return domain[0]['mainLicence']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python3 icp.py -d domain/name',description='icp备案域名查询',)
    p = parser.add_argument_group('icp 的参数')
    p.add_argument("-d", "--domain", type=str, help="查询域名备案单位下的其他域名")
    p.add_argument("-n", "--name", type=str, help="查询该备案单位下的域名")
    p.add_argument("-i", "--icp", type=str, help="备案号查域名")
    p.add_argument("-f", "--file", type=str, help="查询多个单位的域名")
    args = parser.parse_args()
    if args.domain:
        get_domain(get_icp(args.domain))
    if args.name:
        get_domain(args.name)
    if args.icp:
        get_domain(args.icp)
    if args.file:
        files = open(args.file,"r",encoding="utf-8").read().split("\n")
        for domain in files:
            print(f"正在查询{domain}")
            get_domain(get_icp(args.domain))
