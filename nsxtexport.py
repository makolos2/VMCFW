### Package Imports ####
import requests
import json
import argparse


### Ready arguments from command line ###
parser = argparse.ArgumentParser(description='Export user created NSX-T Firewall rules and objects for a given VMC SDDC.')
parser.add_argument('orgid')
parser.add_argument('sddcid')
parser.add_argument('refreshtoken')

args = parser.parse_args()

### Access Token ###
authurl = 'https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize?refresh_token=%s' %(args.refreshtoken)
headers = {'Accept': 'application/json'}
payload = {}
authresp = requests.post(authurl,headers=headers,data=payload)
authjson = json.loads(authresp.text)
token = authjson["access_token"]

### Get ReverseProxy URL ###
infourl = 'https://vmc.vmware.com/vmc/api/orgs/%s/sddcs/%s' %(args.orgid,args.sddcid)
headers = {'csp-auth-token': token, 'content-type': 'application/json'}
payload = {}
sddcresp = requests.get(infourl,headers=headers,data=payload)
sddcjson = json.loads(sddcresp.text)
srevproxyurl = sddcjson["resource_config"]["nsx_api_public_endpoint_url"]


### Source SDDC URL's ###
smgwgroupsurl = '%s/policy/api/v1/infra/domains/mgw/groups' %(srevproxyurl)
scgwgroupsurl = '%s/policy/api/v1/infra/domains/cgw/groups' %(srevproxyurl)
scgwurl = '%s/policy/api/v1/infra/domains/cgw/gateway-policies/default/rules' %(srevproxyurl)
smgwurl = '%s/policy/api/v1/infra/domains/mgw/gateway-policies/default/rules' %(srevproxyurl)
sservicesurl = '%s/policy/api/v1/infra/services' %(srevproxyurl)
sdfwurl = '%s/policy/api/v1/infra/domains/cgw/communication-maps' %(srevproxyurl)

headers = {'csp-auth-token': token, 'content-type': 'application/json'}

sfwDump = open("sourceRules.json", "a+")
### Get Source MGW Groups ###
mgroupsresp = requests.get(smgwgroupsurl,headers=headers)
mg = json.loads(mgroupsresp.text)
mgroups = mg["results"]


### Filter out system groups ###
print("MGW Groups")
for group in mgroups:
    if group["_create_user"]!= "admin" and group["_create_user"]!="admin;admin":
        print(json.dumps(group,indent=4))

### Get Source CGW Groups ###
cgroupsresp = requests.get(scgwgroupsurl,headers=headers)
cg = json.loads(cgroupsresp.text)
cgroups = cg["results"]

### Filter out system groups ###
print("CGW Groups")
for group in cgroups:
    if group["_create_user"]!= "admin" and group["_create_user"]!="admin;admin":
        print(json.dumps(group,indent=4))

### Get Source SDDC Firewall Services ###
servicesresp = requests.get(sservicesurl,headers=headers)
srv = json.loads(servicesresp.text)
services = srv["results"]

### Filter out system Services ###
print("Services")
for service in services:
    if service["_create_user"]!= "admin" and service["_create_user"]!="admin;admin" and service["_create_user"]!="system":
        print(json.dumps(service,indent=4))

### Get Management Gateway Firewall Rules ###    
mgwresponse = requests.get(smgwurl,headers=headers)
m = json.loads(mgwresponse.text)
mgwrules = m["results"]

### Filter out system Rules ###
print("MGW Rules")
for rule in mgwrules:
    if rule["_create_user"]!= "admin" and rule["_create_user"]!="admin;admin" and rule["_create_user"]!="system":
        print(json.dumps(rule,indent=4))
    
### Get Compute Gateway Firewall Rules ###
cgwresponse = requests.get(scgwurl,headers=headers)
c = json.loads(cgwresponse.text)
cgwrules = c["results"]
    
### Filter out system Rules ###
print("CGW Rules")
for rule in cgwrules:
    if rule["_create_user"]!= "admin" and rule["_create_user"]!="admin;admin" and rule["_create_user"]!="system":
        print(json.dumps(rule,indent=4))
        
### Get Source Distributed Firewall Rules ###
dfwresponse = requests.get(sdfwurl,headers=headers)
d = json.loads(dfwresponse.text)
cmaps = d["results"]
print("DFW Rules")
for cmap in cmaps:
    print(json.dumps(cmap,indent=4))

