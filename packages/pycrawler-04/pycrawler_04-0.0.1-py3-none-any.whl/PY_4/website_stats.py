#!/usr/bin/env python
try:
    from . import command_parser as cp
except:
    import command_parser as cp
    

def run():
    cp.cmd_execute()

if __name__ == '__main__':
    run()


