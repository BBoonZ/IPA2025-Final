from netmiko import ConnectHandler
from pprint import pprint

router_ip = ""
device_params = {}

def set_router_ip(ip):
    global router_ip 
    global device_params

    router_ip = ip

    device_params = {
    "device_type": "cisco_ios",
    "ip": router_ip,
    "username": "admin",
    "password": "cisco",
    "conn_timeout": 20,
    "banner_timeout": 30
}

def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        for status in result:
            if "GigabitEthernet" in status['interface']:
                admin_stace = status['status'].lower()
                ans += f"{status['interface']} {admin_stace}, "

                if admin_stace == "up":
                    up += 1
                elif admin_stace == "down":
                    down += 1
                elif admin_stace == "administratively down":
                    admin_down += 1

        ans = f"{ans[:-2]} -> {up} up, {down} down, {admin_down} administratively down"

        pprint(ans)
        return ans
