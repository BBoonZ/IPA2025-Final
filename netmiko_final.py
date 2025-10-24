from netmiko import ConnectHandler
from pprint import pprint
import textfsm
from io import StringIO

router_ip = ""
student_id = ""
device_params = {}

banner_template = """
Value Filldown BANNER (.+)

Start
  ^banner motd \^(?P<BANNER>.*)\^ -> Record
"""

def set_router_ip(ip, id):
    global router_ip 
    global student_id 
    global device_params

    router_ip = ip
    student_id = id

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

def motd():
    with ConnectHandler(**device_params) as ssh:
        output = ssh.send_command("show running-config | include banner motd")
        print("Raw output:", output)

        fsm = textfsm.TextFSM(StringIO(banner_template))
        parsed = fsm.ParseText(output)

        if parsed:
            # parsed จะเป็น list of list
            motd_text = parsed[0][0].strip()
            print(f"MOTD on {router_ip}: {motd_text}")
            return motd_text
        else:
            print(f"No MOTD configured on {router_ip}")
            return "Error: No MOTD Configured"

