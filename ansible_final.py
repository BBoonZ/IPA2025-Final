import subprocess
import os

def showrun(router_ip):
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'playbook.yaml', '-i', 'hosts', '--extra-vars', f'router_ip={router_ip}']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "ok"
    else:
        return "Error: Ansible"

if __name__ == "__main__":
    showrun()
