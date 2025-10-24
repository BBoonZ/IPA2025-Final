from ncclient import manager
import xmltodict

m = None

def connect_router(ip, port=830, username="admin", password="cisco"):
    global m

    if m:
        try:
            m.close_session()
        except:
            pass

    try:
        m = manager.connect(
            host=ip,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,
        )
        print(f"Connected to router {ip} via NETCONF")
        return m
    except Exception as e:
        print(f"Cannot connect to router {ip}:", e)
        m = None
        return None

def create(ip):
    m = connect_router(ip)
    if m is None:
        return "Cannot create: NETCONF session failed"

    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070108</name>
                <description>Created via NETCONF</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>172.10.8.1</ip>
                        <netmask>255.255.255.0</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070108 is created successfully using Netconf"
        else:
            return "Cannot create: Interface loopback 66070108"
    except Exception as e:
        print("Error!", e)


def delete(ip):
    m = connect_router(ip)
    if m is None:
        return "Cannot create: NETCONF session failed"

    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback66070108</name>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070108 is deleted successfully using Netconf"
        else:
            return "Cannot delete: Interface loopback 66070108"
    except:
        print("Error!")


def enable(ip):
    m = connect_router(ip)
    if m is None:
        return "Cannot create: NETCONF session failed"

    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070108</name>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070108 is enabled successfully using Netconf"
        else:
            return "Cannot enable: Interface loopback 66070108"
    except:
        print("Error!")


def disable(ip):
    m = connect_router(ip)
    if m is None:
        return "Cannot create: NETCONF session failed"

    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070108</name>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070108 is shutdowned successfully using Netconf"
        else:
            return "Cannot shutdown: Interface loopback 66070108"
    except:
        print("Error!")

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)


def status(ip):
    m = connect_router(ip)
    if m is None:
        return "Cannot create: NETCONF session failed"

    netconf_filter = """
    <filter>
      <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
          <name>Loopback66070108</name>
        </interface>
      </interfaces>
    </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        # print(netconf_reply)

        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # print(netconf_reply_dict)
        interface_data = netconf_reply_dict.get('rpc-reply', {}).get('data', {}).get('interfaces', {}).get('interface', None)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        # print(interface_data)
        if interface_data:
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = interface_data.get('admin-status')
            oper_status = interface_data.get('oper-status')
            
            if admin_status == 'if-state-up' and oper_status == 'if-oper-state-ready':
                return "Interface loopback 66070108 is enabled (checked by Netconf)"
            elif admin_status == 'if-state-down':
                return "Interface loopback 66070108 is disabled (checked by Netconf)"
        else: # no operation-state data
            return "No Interface loopback 66070108"
    except Exception as e:
       print("Error!", e)

# re = status("10.0.15.62")
# print(re)