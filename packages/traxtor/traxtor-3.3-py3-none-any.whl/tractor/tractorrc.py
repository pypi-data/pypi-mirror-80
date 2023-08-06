#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020

import os
import tempfile
import checks
from bridges import get_file as get_bridge_file

def create():
    dconf = checks.dconf()
    accept_connection = dconf.get_boolean("accept-connection")
    if accept_connection:
        ip = "0.0.0.0"
    else:
        ip = "127.0.0.1"
    socks_port = str(dconf.get_int("socks-port"))
    dns_port = str(dconf.get_int("dns-port"))
    http_port = str(dconf.get_int("http-port"))
    exit_node = dconf.get_string("exit-node")
    bridges_file = get_bridge_file()
    with open(bridges_file) as file:
        bridges = file.read()
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "tractorrc")
    with open(path, 'w') as file:
        socks_port_line = "SocksPort {}:{}\n".format(ip, socks_port)
        file.write(socks_port_line)
        if accept_connection:
            file.write("SocksPolicy accept *\n")
        dns_port_lines = "DNSPort {}:{}\nAutomapHostsOnResolve 1\nAutomapHostsSuffixes .exit,.onion\n".format(ip, dns_port)
        file.write(dns_port_lines)
        http_port_line = "HTTPTunnelPort {}:{}\n".format(ip, http_port)
        file.write(http_port_line)
        if exit_node != "ww":
            exit_node_policy = "ExitNodes {}{}{}\nStrictNodes 1".format('{', exit_node, '}')
            file.write(exit_node_policy)
        if dconf.get_boolean("use-bridges"):
            file.write("UseBridges 1\n")
            obfs4_path = dconf.get_string("obfs4-path")
            file.write("ClientTransportPlugin obfs4 exec {}\n".format(obfs4_path))
            file.write(bridges)
    return tmpdir, path
