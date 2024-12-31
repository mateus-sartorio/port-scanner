import socket
import ipaddress
from common_ports import ports_and_services

def is_ip_address(target):
    return not any(char.isalpha() for char in target)

def is_valid_ip_address(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    socket.setdefaulttimeout(1)

    is_target_ip_address = is_ip_address(target)

    if is_target_ip_address:
        if not is_valid_ip_address(target):
            return "Error: Invalid IP address"
    
    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            result = s.connect_ex((target, port))

            if result == 0:
                open_ports.append(port)
            
        except:
            return "Error: Invalid hostname"
        finally:
            s.close()
    
    if not verbose:
        return open_ports

    verbose_output_header = ""
    try:
        url = socket.gethostbyaddr(target)[0] if is_target_ip_address else target
        ip_address = target if is_target_ip_address else socket.gethostbyname(target)
        verbose_output_header = f"Open ports for {url} ({ip_address})"
    except:
        verbose_output_header = f"Open ports for {target}"
    
    verbose_output = f"{verbose_output_header}\nPORT     SERVICE"

    for port in open_ports:
        service_name = ports_and_services[port]
        padded_port = f"{port}".ljust(9)
        verbose_output += f"\n{padded_port}{service_name}"

    return verbose_output