#!/usr/bin/env python
'''Get instructors per bootcamp from cached bootcamp info.'''
import sys
import yaml

def main():
    '''Main driver.'''
    bootcamps = yaml.load(sys.stdin)
    for b in bootcamps:
        for i in b['instructor']:
            print "%s,'%s'" % (b['slug'], i)

if __name__ == '__main__':
    main()
