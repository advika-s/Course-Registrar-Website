#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Alice Lee, Advika Srivastava
#-----------------------------------------------------------------------

import sys
import argparse
import reg

#-----------------------------------------------------------------------

def _parse_args():
    '''Takes nothing as input. Parses arguments using argparse.
    Returns port.
    '''
    try:
        parser = argparse.ArgumentParser(allow_abbrev=False,
            description='The registrar application')
        parser.add_argument('port',type=int, metavar='port',
            help="the port at which the server should listen")

        args = parser.parse_args()
        port = args.port
        return port
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

def main():
    port = _parse_args()
    try:
        reg.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__=='__main__':
    main()
