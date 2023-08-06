#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020

import fire
import sys
import actions
import proxy
import checks
import bridges

def main():
    if len(sys.argv) == 2:
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
    else:
        print('Tractor needs one argument.')
        sys.exit(1)

if __name__ == '__main__':
    main()
