import json
import requests
import os
from dotenv import load_dotenv
requests.packages.urllib3.disable_warnings()

load_dotenv()

router_ip = ""

api_url = f"https://{router_ip}/restconf/data"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")

def set_router_ip(ip):
    global router_ip 
    global api_url
    
    router_ip = ip
    api_url = f"https://{router_ip}/restconf/data"

def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070108",
            "description": "Created Loopback66070108",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {"ip": "172.10.8.1", "netmask": "255.255.255.0"}
                ]
            }
        }
    }

    resp = requests.put(
        f"{api_url}/ietf-interfaces:interfaces/interface=Loopback66070108",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070108 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070108"


def delete():

    resp = requests.delete(
        f"{api_url}/ietf-interfaces:interfaces/interface=Loopback66070108",
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070108 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070108"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070108",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }

    resp = requests.patch(
        f"{api_url}/ietf-interfaces:interfaces/interface=Loopback66070108",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070108 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070108"


def disable():

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070108",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.patch(
        f"{api_url}/ietf-interfaces:interfaces/interface=Loopback66070108",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070108 is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 66070108"


def status():
    resp = requests.get(
        f"{api_url}/ietf-interfaces:interfaces-state/interface=Loopback66070108",
        auth=basicauth,
        headers=headers,
        verify=False,
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070108 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070108 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070108"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Undefined Error"