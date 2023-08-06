#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020

import os
import signal
import sys
from . import tractorrc
from . import checks
from stem.process import launch_tor
from stem.util import term

def print_bootstrap_lines(line):
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE), flush=True)

def start():
    '''
    starts onion routing
    '''
    if checks.running():
        print(term.format("Tractor is already started", term.Attr.BOLD, term.Color.GREEN))
        sys.exit(0)
    else:
        tmpdir, torrc = tractorrc.create()
        attempts=5
        dconf = checks.dconf()
        print(term.format("Starting Tractor:\n", term.Attr.BOLD, term.Color.YELLOW))
        try:
            tractor_process = launch_tor(
                torrc_path = torrc,
                init_msg_handler = print_bootstrap_lines,
                timeout = 120,
            )
            dconf.set_int("pid", tractor_process.pid)
        except OSError:
            print(term.format("Reached timeout.\n", term.Color.RED))
            sys.exit(1)
        except KeyboardInterrupt:
            os.remove(torrc)
            os.rmdir(tmpdir)
            sys.exit(1)
        os.remove(torrc)
        os.rmdir(tmpdir)
    if checks.running():
        print(term.format("Tractor is conneted.", term.Attr.BOLD, term.Color.GREEN))
        sys.exit(0)
    else:
        print(term.format("Tractor could not connect. Please check your connection and try again.", term.Attr.BOLD, term.Color.RED))
        sys.exit(1)

def stop():
    '''
    stops onion routing
    '''
    if checks.running():
        dconf = checks.dconf()
        pid = dconf.get_int("pid")
        os.kill(pid, signal.SIGTERM)
        dconf.set_int("pid", 0)
        print(term.format("Tractor stopped", term.Attr.BOLD, term.Color.YELLOW))
        sys.exit(0)
    else:
        print("Tractor seems to be stopped.")
        sys.exit(0)

def restart():
    '''
    stop, then start
    '''
    stop()
    start()

def new_id():
    '''
    gives user a new identity
    '''
    if checks.running():
        dconf = checks.dconf()
        pid = dconf.get_int("pid")
        os.kill(pid, signal.SIGHUP)
        print(term.format("You have a new identity now!", term.Attr.BOLD, term.Color.BLUE))
        sys.exit(0)
    else:
        print("Tractor is stopped.")
        sys.exit(1)

def kill_tor():
    '''
    kill all tor processes by user
    '''
    for proc in checks.procs():
        os.killpg(os.getpgid(proc['pid']), signal.SIGTERM)
