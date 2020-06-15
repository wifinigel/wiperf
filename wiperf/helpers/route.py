
from socket import gethostbyname
import subprocess
import re

def check_route_to_dest(ip_address, file_logger):

    # If ip address is a hostname rather than an IP, do a lookup and substitute IP
    if re.search(r'[a-z]|[A-Z]', ip_address):
        hostname = ip_address
        # watch out for DNS Issues
        try:
            ip_address = gethostbyname(hostname)
            file_logger.info(
                "DNS hostname lookup : {}. Result: {}".format(hostname, ip_address))
        except Exception as ex:
            file_logger.error(
                "Issue looking up host {} (DNS Issue?): {}".format(hostname, ex))
            return False

    ip_route_cmd = "/bin/ip route show to match " + \
        ip_address + " | head -n 1 | awk '{print $5}'"

    try:
        interface_name = subprocess.check_output(ip_route_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        file_logger.info("Checked interface route to : {}. Result: {}".format(ip_address, interface_name.strip()))
        return interface_name.strip()
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode()
        file_logger.error("Issue looking up route (route cmd syntax?): {} (command used: {})".format(str(output), ip_route_cmd))
        return ''