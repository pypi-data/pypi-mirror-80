#!/usr/bin/python3
#2020 Danial Behzadi
#Released under GPLv3+

from gi.repository import Gio, GLib
import os
import fire
from getpass import getuser
from psutil import Process, process_iter
import requests
from shutil import copyfile
import signal
import stem.process
from stem.util import term
import sys
import tempfile
import time

dconf=1

def set_schema():
    global dconf
    schema = 'org.tractor'
    schemas = Gio.SettingsSchemaSource.get_default()
    if Gio.SettingsSchemaSource.lookup(schemas, schema, False):
        dconf = Gio.Settings.new(schema)
    else:
        print('''
        Please compile the "tractor.gschema.xml" file.
        In GNU/Linux you can copy it to "/usr/share/glib-2.0/schemas/"
        and run "sudo glib-compile-schemas /usr/share/glib-2.0/schemas/".
        The file is located at {}.
        '''.format(os.path.dirname(os.path.abspath(__file__))))
        sys.exit(404)

def my_tor_procs():
    return [p.info for p in process_iter(attrs=['pid', 'name', 'username']) if p.info['name']=='tor' and p.info['username']==getuser()]

def is_running():
    pid = dconf.get_int("pid")
    if pid == 0:
        return False
    else:
        tor_procs = my_tor_procs()
        if pid in [proc['pid'] for proc in tor_procs]:
            return True
        else:
            return False

def is_connected():
    if is_running():
        port = dconf.get_int("socks-port")
        host = "https://check.torproject.org/"
        proxy = "socks5h://127.0.0.1:{}".format(port)
        expectation = "Congratulations."
        try:
            request = requests.get(host,
                    proxies={"http": proxy, "https": proxy},
                    timeout=10)
            if request.status_code == 200 and expectation in request.text:
                return True
            else:
                return False
        except:
            return False
    else:
        return False

def kill_tor():
    for proc in my_tor_procs():
        os.killpg(os.getpgid(proc['pid']), signal.SIGTERM)

def get_sample_bridges():
    return os.path.dirname(os.path.abspath(__file__))+"/SampleBridges"

def copy_sample_bridges():
    sample_bridges_file = get_sample_bridges()
    try:
        copyfile(sample_bridges_file, bridges_file)
    except IOError as e:
        print("There is an error: %s" % e)
        sys.exit(1)

def get_bridges_file():
    config_dir = GLib.get_user_config_dir() + "/tractor"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    bridges_file = config_dir + "/Bridges"
    if not os.path.isfile(bridges_file):
        copy_sample_bridges()
    return bridges_file


def create_tractorrc():
    accept_connection = dconf.get_boolean("accept-connection")
    if accept_connection:
        ip = "0.0.0.0"
    else:
        ip = "127.0.0.1"
    socks_port = str(dconf.get_int("socks-port"))
    dns_port = str(dconf.get_int("dns-port"))
    http_port = str(dconf.get_int("http-port"))
    exit_node = dconf.get_string("exit-node")
    bridges_file = get_bridges_file()
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

def print_bootstrap_lines(line):
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE), flush=True)

def start():
    if is_running():
        print(term.format("Tractor is already started", term.Attr.BOLD, term.Color.GREEN))
        sys.exit(0)
    else:
        tmpdir, tractorrc = create_tractorrc()
        attempts=5
        print(term.format("Starting Tractor:\n", term.Attr.BOLD, term.Color.YELLOW))
        try:
            tractor_process = stem.process.launch_tor(
                torrc_path = tractorrc,
                init_msg_handler = print_bootstrap_lines,
                timeout = 120,
            )
            dconf.set_int("pid", tractor_process.pid)
        except OSError:
            print(term.format("Reached timeout.\n", term.Color.RED))
            sys.exit(1)
        except KeyboardInterrupt:
            os.remove(tractorrc)
            os.rmdir(tmpdir)
            sys.exit(1)
        os.remove(tractorrc)
        os.rmdir(tmpdir)
    if is_running():
        print(term.format("Tractor is conneted.", term.Attr.BOLD, term.Color.GREEN))
        sys.exit(0)
    else:
        print(term.format("Tractor could not connect. Please check your connection and try again.", term.Attr.BOLD, term.Color.RED))
        sys.exit(1)

def stop():
    if is_running():
        pid = dconf.get_int("pid")
        os.kill(pid, signal.SIGTERM)
        dconf.set_int("pid", 0)
        print(term.format("Tractor stopped", term.Attr.BOLD, term.Color.YELLOW))
        sys.exit(0)
    else:
        print("Tractor seems to be stopped.")
        sys.exit(0)

def restart():
    stop()
    start()

def new_id():
    if is_running():
        pid = dconf.get_int("pid")
        os.kill(pid, signal.SIGHUP)
        print(term.format("You have a new identity now!", term.Attr.BOLD, term.Color.BLUE))
        sys.exit(0)
    else:
        print("Tractor is stopped.")
        sys.exit(1)

def pset():
    proxy = Gio.Settings.new("org.gnome.system.proxy")
    socks = Gio.Settings.new("org.gnome.system.proxy.socks")
    dconf = Gio.Settings.new("org.tractor")
    accept_connection = dconf.get_boolean("accept-connection")
    if accept_connection:
        ip = "0.0.0.0"
    else:
        ip = "127.0.0.1"
    socks_port = dconf.get_int("socks-port")
    ignored = ['localhost', '127.0.0.0/8', '::1', '192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12']
    socks.set_string("host", ip)
    socks.set_int("port", socks_port)
    proxy.set_string("mode", "manual")
    proxy.set_strv("ignore-hosts", ignored)
    print("Proxy set")

def unset():
    proxy = Gio.Settings.new("org.gnome.system.proxy")
    proxy.set_string("mode", "none")
    print("Proxy unset")

def main():
    if len(sys.argv) == 2:
        set_schema()
        fire.Fire({
            'start': start,
            'stop': stop,
            'newid': new_id,
            'restart': restart,
            'set': pset,
            'unset': unset,
            'isrunning': is_running,
            'isconnected': is_connected,
            'bridgesfile': get_bridges_file,
            'killtor': kill_tor,
            })
    else:
        print('Tractor needs one argument.')
        sys.exit(1)

if __name__ == '__main__':
    main()
