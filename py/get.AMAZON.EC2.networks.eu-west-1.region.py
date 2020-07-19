#!/usr/bin/env python

import requests

def amazonIPs(base_url):
    r=requests.get(base_url).json()['prefixes']
    amazon_ip_list=[]
    for item in r:
        if item["service"] == "AMAZON" and item['region'] == "eu-west-1":
            amazon_ip_list.append(item['ip_prefix'])
    return amazon_ip_list

def ec2IPs(base_url):
    ec2_ip_list=[]
    r=requests.get(base_url).json()['prefixes']
    for item in r:
        if item['service'] == "EC2" and item['region'] == "eu-west-1":
            ec2_ip_list.append(item['ip_prefix'])
    return ec2_ip_list

def amazonEC2(base_url):
    amazon=amazonIPs(base_url)
    ec2=ec2IPs(base_url)
    combined=[]
    for a in ec2:
        if a in amazon:
            combined.append(a)
    return combined

def main():
    base_url="https://ip-ranges.amazonaws.com/ip-ranges.json"
    amazon=amazonIPs(base_url)
    amazon.sort()
    ec2=ec2IPs(base_url)
    ec2.sort()
    combined=amazonEC2(base_url)
    combined.sort()
    print("\n")
    print("EC2 networks in EU-WEST-1 Region: ")
    print("----------------------------------")
    print(*ec2, sep='\n')
    print("\n")
    print("AMAZON networks in EU-WEST-1 Region: ")
    print("-------------------------------------")
    print(*amazon, sep='\n')
    print("\n")
    print("Matching Amazon and EC2 in EU-WEST-1 Region")
    print("-------------------------------------------")
    print(*combined, sep='\n')

if __name__ == '__main__':
    main()
