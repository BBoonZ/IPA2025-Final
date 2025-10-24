import subprocess
import os

def showrun(router_ip):
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'playbook.yaml', '-i', 'hosts', '--extra-vars', f'router_ip={router_ip}']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "Ok: success"
    else:
        return "Error: Ansible"

def motd(router_ip, student_id):
    command = ['ansible-playbook', 'playbook-2025.yaml', '-i', 'hosts', '--extra-vars', f'router_ip={router_ip} student_id={student_id}']
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        return "Ok: success"
    else:
        return f"Error: Ansible\n{result.stdout}\n{result.stderr}"

if __name__ == "__main__":
    showrun()
