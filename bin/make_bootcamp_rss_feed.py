#!/usr/bin/env python
'''
Create bootcamp-feed.xml for RSS feed for Software Carpentry 
boot camps.
'''

import datetime
import os
import sys
import re
import yaml
from optparse import OptionParser
from PyRSS2Gen import RSS2, RSSItem, Guid
from make_rss_feed import ContentEncodedRSS2, ContentEncodedRSSItem
try:  # Python 3
    from urllib.parse import urlparse
except ImportError:  # Python 2
    from urlparse import urlparse
from util import CONFIG_YML, STANDARD_YML, load_info

#----------------------------------------

def main():
    '''Main driver for boot camp feed regeneration.'''

    options, args = parse_args()
    config = load_info(os.curdir)
    config['site'] = options.site

    build_bootcamp_rss(config,
                       os.path.join(options.output, 'bootcamp-feed.xml'))

    # TODO - TEST TO UPDATE BOOTCAMP_URLS
    # TODO - SORT INTO DATE ORDER
    # TODO - CLEAN UP RSS FEED CONTENT
    # TODO - PARSE FEED FOR COMPLIANCE
    # TODO - resolve country
    # TODO - resolve pubDate w.r.t specification
    # TODO - replace title and description
    # http://cyber.law.harvard.edu/rss/rss.html
    # http://www.w3schools.com/rss/rss_item.asp
    # python bin/make_bootcamps.py -o _site/ -s _site/

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

def build_bootcamp_rss(config, filename):
    '''
    Generate RSS2 file for bootcamps given the metadata blobs for
    recent bootcamps.
    '''
    items = []
    site = config['site']
    for bc in config['bootcamps']:
        if bc['country'] == 'United-Kingdom':
            # Create RSS items.
            at = ''
            if bc.get('address'):
                at = 'at {0}'.format(bc['address'])
            instructors = ''
            if bc.get('instructor'):
                instructors='led by {0}'.format(', '.join(bc['instructor']))
            description = 'A boot camp will be held on {0} {1} {2}'.format(bc['humandate'], at, instructors)
            guid = Guid('{0}/{1}'.format(site,bc['slug']), isPermaLink=False)
            items.append(ContentEncodedRSSItem(title=bc['venue'],
#                                               creator=bc['contact'],
                                               author=bc['contact'],
                                               guid=guid,
                                               link=bc['url'],
                                               description=description,
                                               content=bc['country'],
#                                               category=bc['country'],
                                               pubDate=datetime.datetime.fromordinal(bc['startdate'].toordinal())))

    # Create RSS feed.
    rss = ContentEncodedRSS2(title='Software Carpentry boot camps',
                             description='Helping researchers do more, in less time, with less pain',
                             lastBuildDate=datetime.datetime.utcnow(),
                             link=site,
                             items=items)

    # Save.
    with open(filename, 'w') as writer:
        rss.write_xml(writer)

#----------------------------------------

if __name__ == '__main__':
    main()
