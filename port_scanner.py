import socket
from common_ports import ports_and_services

import re

def Is_Target_Valid(target):
    """Check if the string is an address (IP or hostname)"""
    ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
    if re.match(ip_pattern, target):
        try:
            socket.inet_aton(target)
            try :
                hostname, _, _ = socket.gethostbyaddr(target)
                return  [target,hostname], True   
            except socket.error :
                return [target,""],True
        except socket.error:
            return ["Error: Invalid IP address"], False
    else:
        try:
            target_ip = socket.gethostbyname(target)
            return [target_ip,target], True
        except socket.gaierror:
            return ["Error: Invalid hostname"], False


def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    res, valid = Is_Target_Valid(target)
   
    if valid:
        target_hostname = res[1]
        target_ip = res[0]
        for port in range(port_range[0], port_range[1] + 1):
            # Create a new socket for each connection attempt
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)  # Timeout for each connection attempt
            
            result = s.connect_ex((target_ip, port))
            #print(result)
            if result == 0:
                open_ports.append(port)
            s.close()  # Close the socket after each connection attempt
        
        if not verbose:
            return open_ports
        else:

            if target_hostname :       
                result_with_verbose = f"Open ports for {target_hostname} ({target_ip})\nPORT     SERVICE\n"
            else :                          
                result_with_verbose = f"Open ports for {target_ip}\nPORT     SERVICE\n" 
            for index, open_port in enumerate(open_ports):
                if index == 0:
                    result_with_verbose += f"{open_port}       {ports_and_services[open_port]}"
                else:
                    result_with_verbose += f"\n{open_port}       {ports_and_services[open_port]}"
            return result_with_verbose
            
    else:
        return res[0]

