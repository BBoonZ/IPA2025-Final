from netmiko import ConnectHandler
from pprint import pprint

router_ip = ""
student_id = ""
device_params = {}

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
        print(output)

        start = output.find("^C")
        end = output.find("^C", start + 2)

        if start != -1 and end != -1:
            motd_text = output[start + 2:end]
            print(f"MOTD on {router_ip}: {motd_text}")
            return motd_text
        else:
            print(f"No MOTD configured on {router_ip}")
            return "Error: No MOTD Configured"

