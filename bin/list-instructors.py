#!/usr/bin/env python
'''Get instructors per workshop from cached workshop info.'''
import sys
import yaml

def main():
    '''Main driver.'''
    workshops = yaml.load(sys.stdin)
    for b in workshops:
        for i in b['instructor']:
            print "%s,'%s'" % (b['slug'], i)

if __name__ == '__main__':
    main()
