#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020

import fire
import sys
from . import actions
from . import bridges
from . import checks
from . import proxy

def main():
    fire.Fire({
        'start': actions.start,
        'stop': actions.stop,
        'newid': actions.new_id,
        'restart': actions.restart,
        'set': proxy.set,
        'unset': proxy.unset,
        'isrunning': checks.running,
        'isconnected': checks.connected,
        'bridgesfile': bridges.get_file,
        'killtor': actions.kill_tor,
        })

if __name__ == '__main__':
    main()
