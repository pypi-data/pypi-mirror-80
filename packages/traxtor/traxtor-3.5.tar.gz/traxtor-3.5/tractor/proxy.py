#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020

from . import checks
from gi.repository import Gio

def set():
    proxy = Gio.Settings.new('org.gnome.system.proxy')
    socks = Gio.Settings.new('org.gnome.system.proxy.socks')
    dconf = checks.dconf()
    accept_connection = dconf.get_boolean('accept-connection')
    if accept_connection:
        ip = '0.0.0.0'
    else:
        ip = '127.0.0.1'
    socks_port = dconf.get_int('socks-port')
    ignored = ['localhost', '127.0.0.0/8', '::1', '192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12']
    socks.set_string('host', ip)
    socks.set_int('port', socks_port)
    proxy.set_string('mode', 'manual')
    proxy.set_strv('ignore-hosts', ignored)
    print('Proxy set')

def unset():
    proxy = Gio.Settings.new('org.gnome.system.proxy')
    proxy.set_string('mode', 'none')
    print('Proxy unset')
