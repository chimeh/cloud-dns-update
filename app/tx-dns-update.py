#!/usr/bin/python
# -*- coding: utf-8 -*-
# borrow code from https://github.com/patrickwangqy/AutoUpdateDomain.git
# whith modify by hjm
from QcloudApi.qcloudapi import QcloudApi
import requests
import json
import os
import datetime
import time
import argparse
import sys
from socket import gethostbyname
reload(sys) 
sys.setdefaultencoding('utf8') 
#get your true IP
def get_out_ip():
    session = requests.Session()
    session.trust_env = False
    response = session.get('http://ifconfig.co/ip')
    myip = response.text.strip()
    return "%s" % myip
    
def get_resolve_ip(host):
    try:
        resolve_ip = gethostbyname(host)
    except Exception as e:
        resolve_ip = "0.0.0.0"
    finally:
        return "%s" % resolve_ip

#refer to https://github.com/QcloudApi/qcloudapi-sdk-python
def get_cns_service(secretId,secretKey):
    module = 'cns'
    config = {
        'Region': 'ap-beijing',
        'secretId':secretId,
        'secretKey':secretKey,
        'method': 'get'
    }
    service = QcloudApi(module, config)
    return service

#refers to https://cloud.tencent.com/document/api/302/8517
def get_record_list(cns_service,domain):
    action = 'RecordList'
    params = {
        'domain':domain,
    }
    return cns_service.call(action, params)
#refers to https://cloud.tencent.com/document/api/302/8516
def add_dns_record_ip(cns_service,domain,subdomain,ip):
    action = 'RecordCreate'
    params = {
        'domain':domain,
        'subDomain':subdomain,
        'recordLine':'默认',
        'recordType':'A',
        'value':ip,
    }
    return cns_service.call(action,params)

#refers to https://cloud.tencent.com/document/api/302/8511
def modify_dns_record_ip(cns_service,domain,subdomain,record_id,ip):
    action = 'RecordModify'
    params = {
        'domain':domain,
        'subDomain':subdomain,
        'recordId':record_id,
        'recordLine':'默认',
        'recordType':'A',
        'value':ip,
    }
    print(params)
    return cns_service.call(action,params)
def monitor_domain(domain, subdomain, secretId, secretKey,my_ip):
    #Need reqeust in https://console.cloud.tencent.com/capi
    host = "%s.%s" % (subdomain, domain)
    
    #buy domain name in https://dnspod.cloud.tencent.com/?from=qcloudProductDns
    
    if my_ip == "0.0.0.0":
        outip = get_out_ip()
    else:
        outip = my_ip
    
    resolve_ip = get_resolve_ip(host)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +": host %s resolve to %s, outip %s" % (host, resolve_ip, outip))

    service = get_cns_service(secretId,secretKey)
    record_list = json.loads(get_record_list(service,domain))
    json.dumps(record_list)

    if resolve_ip != outip:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +": update host %s to outip %s" % (host, outip))
        record_id = 0
        is_ip = False
        for item in record_list["data"]["records"]:
            if item["type"] == 'A' and item["name"] == subdomain:
                is_ip = True
                record_id = item["id"]
                modify_dns_record_ip(service, domain, subdomain, record_id, outip)
                print("[dns_tool]:Modify a record, id: {}".format(record_id))
        if not is_ip:
            add_dns_record_ip(service, domain,subdomain, outip)
            print("[dns_tool]:Create a new ip record for domain: "+subdomain +"."+domain)
    sys.stdout.flush()

def main():
    default_secretid = os.environ.get("SECRETID", 'YOURsecretid')
    default_secretkey = os.environ.get("SECRETKEY", 'YOURsecretkey')
    parser = argparse.ArgumentParser()
    parser.add_argument("--access_key_id", type=str, default=default_secretid)
    parser.add_argument("--access_key_secret", type=str, default=default_secretkey)
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--subdomain", type=str, required=True)
    parser.add_argument("--ip", type=str, default="0.0.0.0")
    parser.add_argument("--sleep", type=int, default=5)
    args = parser.parse_args()
    while True:
        try:
            monitor_domain(args.domain, args.subdomain, args.access_key_id, args.access_key_secret, args.ip)
        except Exception as e:
            pass
        time.sleep(args.sleep)


if (__name__ == '__main__'):
    main()

