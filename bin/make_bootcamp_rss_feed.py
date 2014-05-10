#!/usr/bin/env python
'''
Create bootcamp-feed.xml for RSS feed for Software Carpentry 
boot camps.
'''

import datetime
import os
import sys
from optparse import OptionParser
from PyRSS2Gen import Category, Guid
from make_rss_feed import ContentEncodedRSS2, ContentEncodedRSSItem
try:  # Python 3
    from urllib.parse import urlparse
except ImportError:  # Python 2
    from urlparse import urlparse
from util import load_info

#----------------------------------------

def main():
    '''Main driver for boot camp feed regeneration.'''

    options, args = parse_args()
    config = load_info(os.curdir)
    config['site'] = options.site

    bootcamps = get_future_boot_camps(config['bootcamps'])
    build_bootcamp_rss(config,
                       os.path.join(options.output, 'bootcamp-feed.xml'),
                       bootcamps)

#----------------------------------------

def parse_args():
    '''Parse command-line arguments.'''

    parser = OptionParser()
    parser.add_option('-o', '--output', dest='output', help='output directory')
    parser.add_option('-s', '--site', dest='site', help='base site URL')
    parser.add_option('-v', '--verbose', dest='verbose', help='enable verbose logging',
                      default=False, action='store_true')
    options, args = parser.parse_args()
    return options, args

#----------------------------------------

def build_bootcamp_rss(config, filename, bootcamps):
    '''
    Generate RSS2 file for bootcamps given the metadata blobs for
    recent bootcamps.
    '''
    site = config['site']
    publish_time = datetime.datetime.now()
    # Create RSS items.
    items = [ContentEncodedRSSItem(title=bc['venue'],
                                   creator=bc['contact'],
                                   guid=get_guid(site, bc),
                                   link=bc['url'],
                                   description=get_description(bc),
                                   categories=[get_country(site, bc)],
                                   pubDate=publish_time)
             for bc in bootcamps]

    # Create RSS feed.
    rss = ContentEncodedRSS2(title='Software Carpentry boot camps',
                             description='Helping researchers do more, in less time, with less pain',
                             lastBuildDate=datetime.datetime.utcnow(),
                             link=site,
                             items=items)

    # Save.
    with open(filename, 'w') as writer:
        rss.write_xml(writer)

def get_future_boot_camps(bootcamps):
    '''
    Create a list of boot camps that are in the future and return these
    in reverse chronological order.
    '''
    publish_date = datetime.datetime.now().date()
    bootcamps = [bc for bc in bootcamps if bc['startdate'] >= publish_date]
    bootcamps.reverse()
    return bootcamps

def get_guid(site, bootcamp):
    '''
    Create non-permalink Guid consisting of Software Carpentry 
    site URL and bootcamp identifier ('slug').
    '''
    return Guid('{0}/{1}'.format(site, bootcamp['slug']), 
                isPermaLink=False)

def get_country(site, bootcamp):
    '''
    Create 'country' category in domain 
    http://software-carpentry.org/locations with boot camp's country
    as value.
    '''
    return Category(bootcamp['country'], 
                    '{0}/{1}'.format(site, 'locations'))

def get_description(bootcamp):
    '''
    Create description string with boot camp date, address (if known)
    and instructors (if known).
    '''
    address = ''
    if bootcamp.get('address'):
        address = u'at {0}'.format(bootcamp['address'])
    instructors = ''
    if bootcamp.get('instructor'):
        instructors = u'led by {0}'.format(u','.join(bootcamp['instructor']))
    return u'A boot camp will be held on {0} {1} {2}'.format(
        bootcamp['humandate'], address, instructors)

#----------------------------------------

if __name__ == '__main__':
    main()
