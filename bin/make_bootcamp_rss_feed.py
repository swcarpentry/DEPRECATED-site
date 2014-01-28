#!/usr/bin/env python
'''
Compile the Software Carpentry calendar file.
'''

import sys
import os
import yaml
import datetime
import re
from PyRSS2Gen import RSS2, RSSItem
from optparse import OptionParser
from make_rss_feed import ContentEncodedRSS2, ContentEncodedRSSItem
try:  # Python 3
    from urllib.parse import urlparse
except ImportError:  # Python 2
    from urlparse import urlparse
from util import CONFIG_YML, STANDARD_YML, load_info

#----------------------------------------

def main():
    '''Main driver for calendar regeneration.'''

    options, args = parse_args()
    config = load_info(os.curdir)
    config['site'] = options.site
    text_file = os.path.join(options.output, 'bootcamps.txt')


#    selection = config['blog'][-config['recent_length']:]
#    selection = config['blog'][-config['recent_length']:]
#    selection.reverse()
#    build_blog_rss(config,
#                   os.path.join(options.output, 'bootcamp-feed.xml'),
#                   selection)
    build_bootcamp_rss(config,
                       os.path.join(options.output, 'bootcamp-feed.xml'))

#    bcw = BootCampWriter()
#    bcw(text_file, config)

    # TODO - TEST TO UPDATE BOOTCAMP_URLS
    # TODO - SORT INTO DATE ORDER
    # TODO - CLEAN UP RSS FEED CONTENT
    # TODO - PARSE FEED FOR COMPLIANCE

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
    Generate RSS2 feed.xml file for bootcamps given the metadata blobs for
    recent bootcamps.
    '''

    items = []
    site = config['site']
    for bc in config['bootcamps']:
        if bc['country'] == 'United-Kingdom':
            print bc
#            lines.extend(self.bootcamp(config['site'], config['timestamp'], bc))
            # Create RSS items.
            items.append(ContentEncodedRSSItem(title=bc['venue'],
                                           creator=bc['contact'],
                                           link=bc['url'],
                                           description=', '.join(bc['instructor']),
                                           content=bc['country'],
                                           pubDate=datetime.datetime.fromordinal(bc['startdate'].toordinal())))

    # Create RSS feed.
    rss = ContentEncodedRSS2(title='Boot camps',
                             description='Boot camps',
                             lastBuildDate=datetime.datetime.utcnow(),
                             link=site,
                             items=items)

    # Save.
    with open(filename, 'w') as writer:
        rss.write_xml(writer)


class BootCampWriter(object):
    '''
    Dump information on a boot camp.
    '''
    def __call__(self, filename, config):
        lines = ['BEGIN',]
        for bc in config['bootcamps']:
            if bc['country'] == 'United-Kingdom':
                print bc
                lines.extend(self.bootcamp(config['site'], config['timestamp'], bc))
        lines.extend(['END', ''])
        content = '\r\n'.join(lines)
        # From RFC 5545, section 3.1.4 (Character Set):
        # The default charset for an iCalendar stream is UTF-8.
        with open(filename, 'wb') as writer:
            writer.write(content.encode('utf-8'))

# python bin/make_bootcamps.py -o _site/ -s _site/
### 'country': 'United-Kingdom', 
### 'url': 'http://apawlik.github.io/2014-01-14-manchester/', 
### 'venue': 'University of Manchester', 
# 'instructor': ['Michael Croucher', 'Jos Martin', 'Shoaib Sufi', 'Aleksandra Pawlik'], 
# 'humandate': 'Jan 14-15, 2014', 
# 'contact': 'admin-uk@software-carpentry.org', 
# ---
# 'latlng': '53.467972,-2.233154', 
# 'address': 'Room IT407, Information Technology Building, University of Manchester, Oxford Road, M13 9PL', 
# 'user': 'apawlik', 'registration': 'restricted', 
# 'layout': 'bootcamp', 
# 'slug': '2014-01-14-manchester', 
# 'startdate': datetime.date(2014, 1, 14), 
# 'enddate': datetime.date(2014, 1, 15), 
# 'humantime': '9:00 am - 5:00 pm', 
# 'root': '.'}

    def bootcamp(self, site, timestamp, info):
        uid = '{0}@{1}'.format(info['slug'],
                               urlparse(site).netloc or 'software-carpentry.org')
        if 'enddate' in info:
            end = info['enddate']
        else:  # one day boot camp?
            end = info['startdate']
        end + datetime.timedelta(1)  # non-inclusive end date
        lines = [
            'BOOTCAMP-BEGIN',
#            'UID:{0}'.format(uid),
#            'DTSTAMP:{0}'.format(timestamp),
            'DATE:{0}'.format(info['humandate']),
            'CONTACT:{0}'.format(info['contact']),
            'URL:{0}'.format(info['url']),
            'COUNTRY:{0}'.format(info['country']),
            'VENUE:{0}'.format(info['venue']),
            'INSTRUCTOR:{0}'.format(', '.join(info['instructor'])),
        ]
        if info.get('latlng'):
            latlng = re.sub(r'\s+', '', info['latlng']).replace(',', ';')
            lines.append('GEO:{0}'.format(latlng))
        lines.append('BOOTCAMP-END')
        return lines

    def escape(self, value):
        '''Escape text following RFC 5545.'''
        for char in ['\\', ';', ',']:
            value = value.replace(char, '\\' + char)
        value.replace('\n', '\\n')
        return value

#----------------------------------------

if __name__ == '__main__':
    main()
