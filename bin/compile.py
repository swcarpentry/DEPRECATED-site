#!/usr/bin/env python
'''
Compile the Software Carpentry web site.
'''

import sys
import os
import re
import yaml
import glob
import jinja2
import datetime
import time
from collections import defaultdict
from optparse import OptionParser
from os.path import join
from PyRSS2Gen import RSS2, RSSItem
try:  # Python 3
    from urllib.parse import urlparse, urljoin
except ImportError:  # Python 2
    from urlparse import urlparse, urljoin

# Translate two-digit month identifiers into short names.
MONTHS = {
    '01' : 'Jan', '02' : 'Feb', '03' : 'Mar', '04' : 'Apr',
    '05' : 'May', '06' : 'Jun', '07' : 'Jul', '08' : 'Aug',
    '09' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'
}

# Standard names for metadata files in each directory.
INFO_YML = '_config.yml'

# Standard information put into web site pages.

# Extra information required by the blog.
BLOG_TITLE = 'Software Carpentry'
BLOG_DESCRIPTION = 'Helping scientists make better software since 1998'
RECENT_LENGTH = 10

# Patterns used to extract content and excerpts from compiled blog
# entries.  Using regular expressions is a hack, but is *much* simpler
# than trying to parse and un-parse the XML.
P_BLOG_CONTENT = re.compile(r'<!--\s+start\s+content\s+-->\s+(.+)\s+<!--\s+end\s+content\s+-->', re.DOTALL)
P_BLOG_EXCERPT = re.compile(r'<!--\s+start\s+excerpt\s+-->\s+(.+)\s+<!--\s+end\s+excerpt\s+-->', re.DOTALL)

# Standard search path for Jinja2 templates.  The script occasionally
# pushes and pops extra directories.
SEARCH_PATH = ['.',
               'templates',
               'bc/_includes',
               'bc/_includes/orgs',
               'bc/_includes/people']

# Pattern used to separate metadata in GitHub-friendly headers
# from the content of the page.
P_PAGE = re.compile(r'^---\n(.+)\n---\n(.+)', re.DOTALL)

# Keys of settings to be copied in from bc/_config.yml.
BOOTCAMP_CONFIG_KEYS = [
    'contact',
    'facebook_url',
    'github_url',
    'google_plus_url',
    'rss_url',
    'twitter_name',
    'twitter_url'
]

#============================================================

def main():
    '''Main driver for recompiling web site.'''

    # 'Options' stores everything that would otherwise be a global
    # variable for compilation, including the Jinja2 environment.
    options, args = parse_args()
    options.jinja2_searchpath = SEARCH_PATH

    # Site-wide definitions for template expansion.  Use defaults
    # defined in bootcamps/_config.yml as a starting point.
    options.site = {
        'recent_length'   : RECENT_LENGTH,
        'bootcamps_site'  : 'bc',
        'month_names'     : MONTHS,
        'months'          : sorted(MONTHS.keys()),
        'site'            : options.output,
        'timestamp'       : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'today'           : options.today
    }
    bc_config = load_info('bc')
    for key in BOOTCAMP_CONFIG_KEYS:
        options.site[key] = bc_config[key]
    options.site['swc_prefix'] = options.output
    options.people = bc_config['people']
    options.categories = load_info('blog')['category']

    # Set up for Jinja2 template expansion.
    loader = jinja2.FileSystemLoader(options.jinja2_searchpath)
    env = jinja2.Environment(loader=loader,
                             autoescape=True,
                             undefined=jinja2.StrictUndefined)
    options.env = env

    # Harvest data needed by the main page as well as sub-pages.
    bootcamp_info = harvest_bootcamps()
    blog_info = harvest_blog(options)

    # Lookup table of function information.
    functions = {
        'blog'      : (build_blog,      blog_info),
        'bootcamps' : (build_bootcamps, bootcamp_info),
        'misc'      : (build_misc,      (blog_info, bootcamp_info)),
        '3_0'       : (build_3_0,       None),
        '4_0'       : (build_4_0,       None)
    }

    if options.single_dir is not None:
        builder, extra = functions[options.single_dir]
        builder(options, extra)
    else:
        for name in sorted(functions.keys()):
            builder, extra = functions[name]
            builder(options, extra)

#----------------------------------------

def parse_args():
    '''Parse command-line arguments.'''
    parser = OptionParser()
    parser.add_option('-o', '--output', dest='output', help='output directory')
    parser.add_option('-s', '--single', dest='single_dir', help='build a single directory', default=None)
    parser.add_option('-t', '--today', dest='today', help='build date',
                      default=datetime.date.today())
    parser.add_option('-v', '--verbose', dest='verbose', help='enable verbose logging',
                      default=False, action='store_true')
    options, args = parser.parse_args()
    return options, args

#----------------------------------------

def build_blog(options, all_metas):
    '''Rebuild the blog posts.'''

    if options.verbose:
        print >> sys.stderr, 'blog'

    # Construct 'ordered' and 'lookup' for stitching 'prev'/'next'
    # links together.
    ordered = [m['path'] for m in all_metas]
    lookup = dict([(p, i) for (i, p) in enumerate(ordered)])

    # Render the blog posts.
    for m in all_metas:
        folder, filename = m['folder'], m['path']
        options.env.loader.searchpath.append(folder)
        m['prev'], m['next'] = prev_next(filename, ordered, lookup)
        m['uplink'] = '../../index.html'
        temp = render(options, filename, '../../..', m)
        m['rendered'], m['excerpt'] = build_blog_excerpt(filename, temp)
        options.env.loader.searchpath.pop()

    # Construct feed.xml.
    selection = all_metas[-RECENT_LENGTH:]
    selection.reverse()
    build_blog_rss(options,
                   join(options.output, 'feed.xml'),
                   selection)

    # Construct blog home page.  Along with the usual metadata, this
    # needs a field 'lookup' containing an ordered list of blog posts
    # indexed by (year, month) so that tables and summary lists can be
    # constructed.
    index_m = {
        'years'               : set(),
        'posts'               : all_metas,
        'lookup'              : defaultdict(list)
    }
    index_m.update(harvest('blog/index.html'))
    for m in all_metas:
        index_m['years'].add(m['date'].year)
        index_m['lookup'][(m['date'].year, m['date'].month)].append(m)
    index_m['years'] = sorted(index_m['years'])
    render(options, 'blog/index.html', '..', index_m)

#----------------------------------------

def build_blog_excerpt(filename, content):
    '''
    Extract page content and excerpt from blog post.  This expects the
    template for blog posts to include comments:
    <!-- start content -->
    and
    <!-- end content -->
    It also expects the excerpts includes in the feed.xml file to have:
    <!-- start excerpt -->
    and
    <!-- end excerpt -->
    The latter markers have only been added starting in May 2013;
    earlier blog posts no longer have excerpts included in feed.xml,
    so this function returns None for them.
    '''

    temp = P_BLOG_CONTENT.search(content)
    assert temp, \
           'Blog entry "{0}" lacks content markers'.format('path')
    rendered = temp.group(1)

    temp = P_BLOG_EXCERPT.search(rendered)
    excerpt = None
    if temp:
        excerpt = temp.group(1)

    return rendered, excerpt

#----------------------------------------

def build_blog_rss(options, filename, post_metas):
    '''
    Generate RSS2 feed.xml file for blog given the metadata blobs for
    recent posts.
    '''

    site = options.site['site']
    items = [ContentEncodedRSSItem(title=p['title'],
                                   author=p['author'],
                                   link=join(site, p['path']),
                                   description=p['excerpt'],
                                   content=p['rendered'],
                                   pubDate=str(p['date'])) # FIXME
             for p in post_metas]

    rss = ContentEncodedRSS2(title=BLOG_TITLE,
                             description=BLOG_DESCRIPTION,
                             lastBuildDate=datetime.datetime.utcnow(),
                             link=site,
                             items=items)

    with open(filename, 'w') as writer:
        rss.write_xml(writer)

#----------------------------------------

def build_bootcamps(options, bootcamps):
    '''
    Rebuild the bootcamp index page and calendar feed.  This expects
    date to already be harvested (since that data is also used by the
    main page).  It does *not* compile the bootcamp pages: they are
    expanded by Jekyll on GitHub.
    '''

    if options.verbose:
        print >> sys.stderr, 'bootcamps'

    # Rebuild the bootcamps.html overview page.
    render(options, 'bootcamps/index.html', '.',
           {'bootcamps' : bootcamps,
            'title'     : 'Bootcamps',
            'path'      : 'bootcamps/index.html'})

    # Rebuild the legacy bootcamp home pages.
    for b in bootcamps:
        render(options, b['path'], '../..', b)

    # Recompile the calendar file.
    icw = ICalendarWriter()
    icw(join(options.output, 'bootcamps.ics'),
        options.site,
        bootcamps)

#----------------------------------------

def build_misc(options, extra):
    '''Build miscellaneous files.'''

    if options.verbose:
        print >> sys.stderr, 'miscellaneous'

    # Pull out extra information.
    blog_info, bootcamp_info = extra
    blog_info.reverse() # to get most recent at the front
    blog_info = blog_info[:RECENT_LENGTH]
    bootcamp_info = [b for b in bootcamp_info if b['startdate'] >= options.site['today']]
    bootcamp_info = bootcamp_info[:RECENT_LENGTH]

    # File names and paths upward to the root directory.
    controls = [('badges/index.html', '..')] + \
               [(f, '.') for f in glob.glob('*.html')]

    # Build pages one by one.
    for (filename, root_path) in controls:
        metadata = harvest(filename)
        metadata['posts'] = blog_info
        metadata['bootcamps'] = bootcamp_info
        render(options, filename, root_path, metadata)

#----------------------------------------

def build_3_0(options, unused):
    '''Build Version 3 lessons.'''

    if options.verbose:
        print >> sys.stderr, '3_0'

    files = glob.glob('3_0/*.html')
    for filename in files:
        m = harvest(filename)
        render(options, filename, '..', m)

#----------------------------------------

def build_4_0(options, unused):
    '''Build Version 4 lessons.'''

    if options.verbose:
        print >> sys.stderr, '4_0'

    index_file = join('4_0', 'index.html')
    m = harvest(index_file)
    render(options, index_file, '..', m)

    # Render each lesson and its topics.
    lessons = [os.path.dirname(i) for i in glob.glob('4_0/*/index.html')]
    for les in lessons:
        files = glob.glob('{0}/*.html'.format(les))
        for f in files:
            m = harvest(f)
            render(options, f, '../..', m)

#============================================================

class ContentEncodedRSS2(RSS2):
    '''Represent an RSS2 feed with content-encoded items.'''

    def __init__(self, **kwargs):
        RSS2.__init__(self, **kwargs)
        self.rss_attrs['xmlns:content']='http://purl.org/rss/1.0/modules/content/'

#----------------------------------------

class ContentEncodedRSSItem(RSSItem):
    '''Represent a single item in an RSS2 feed with content encoding.'''

    def __init__(self, **kwargs):
        self.content = kwargs.get('content', None)
        if 'content' in kwargs:
            del kwargs['content']
        RSSItem.__init__(self, **kwargs)

    def publish_extensions(self, handler):
        if self.content:
            if hasattr(handler, '_out'):
                writer = handler._out.write
            elif hasattr(handler, '_write'):
                writer = handler._write
            else:
                assert False, \
                       'XML handler does not have _out or _write'
            writer('<%(e)s><![CDATA[%(c)s]]></%(e)s>' %
                   { 'e':'content:encoded', 'c':self.content})

#============================================================

class ICalendarWriter(object):
    '''
    iCalendar generator for boot camps.
    The format is defined in RFC 5545: http://tools.ietf.org/html/rfc5545
    '''

    def __call__(self, filename, settings, bootcamps):
        lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//Software Carpentry/Boot Camps//NONSGML v1.0//EN',
        ]
        for bootcamp in bootcamps:
            lines.extend(self.bootcamp(settings['site'], settings['timestamp'], bootcamp))
        lines.extend(['END:VCALENDAR', ''])
        content = '\r\n'.join(lines)
        # From RFC 5545, section 3.1.4 (Character Set):
        # The default charset for an iCalendar stream is UTF-8.
        with open(filename, 'wb') as writer:
            writer.write(content.encode('utf-8'))

    def bootcamp(self, site, timestamp, info):
        uid = '{0}@{1}'.format(info['slug'],
                               urlparse(site).netloc or 'software-carpentry.org')
        url = urljoin(site, 'bootcamps/{0}/index.html'.format(info['slug']))
        if 'enddate' in info:
            end = info['enddate']
        else:  # one day boot camp?
            end = info['startdate']
        end + datetime.timedelta(1)  # non-inclusive end date
        lines = [
            'BEGIN:VEVENT',
            'UID:{0}'.format(uid),
            'DTSTAMP:{0}'.format(timestamp),
            'DTSTART;VALUE=DATE:{0}'.format(info['startdate'].strftime('%Y%m%d')),
            'DTEND;VALUE=DATE:{0}'.format(end.strftime('%Y%m%d')),
            'SUMMARY:{0}'.format(self.escape(info['venue'])),
            'DESCRIPTION;ALTREP="{0}":{0}'.format(url),
            'URL:{0}'.format(url),
            'LOCATION:{0}'.format(self.escape(info['venue'])),
        ]
        if 'latlng' in info:
            latlng = re.sub(r'\s+', '', info['latlng']).replace(',', ';')
            lines.append('GEO:{0}'.format(latlng))
        lines.append('END:VEVENT')
        return lines

    def escape(self, value):
        '''Escape text following RFC 5545.'''
        for char in ['\\', ';', ',']:
            value = value.replace(char, '\\' + char)
        value.replace('\n', '\\n')
        return value

#============================================================

def ensure_folder(file_path):
    '''Make sure the folder for a particular file exists.'''
    dir_path = os.path.dirname(file_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

#----------------------------------------

def harvest(filespec):
    '''
    Get content and metadata from HTML files. Return a single metadata
    dictionary if a single path is given as input, or a dictionary
    mapping filenames to metadata dictionaries if multiple paths are
    given.
    '''
    if isinstance(filespec, basestring):
        return harvest_single(filespec)

    elif isinstance(filespec, list):
        return dict([(f, harvest_single(f)) for f in filespec])

    else:
        assert False, 'Unknown filespec "{0}"'.format(filespec)

#----------------------------------------

def harvest_blog(options):
    '''Harvest metadata for all blog entries.'''

    all_meta = []
    for folder in glob.glob('blog/????/??'):
        for post in glob.glob('{0}/*.html'.format(folder)):
            m = harvest_single(post)
            m['folder'] = folder
            m['author'] = options.people[m['author']]
            m['category'] = set([options.categories[c] for c in m['category']])
            all_meta.append(m)

    all_meta.sort(lambda x, y: cmp(x['date'], y['date']) and cmp(x['time'], y['time']))
    return all_meta

#----------------------------------------

def harvest_bootcamps():
    '''Harvest metadata from all boot camp index.html pages.'''
    pages = glob.glob('bootcamps/*/index.html')
    metadata = harvest(pages)
    bootcamps = []
    for f in metadata:
        bootcamps.append(metadata[f])
        bootcamps[-1]['slug'] = f.split('/')[1]
        if 'contact' not in metadata[f]: # FIXME: need to figure out how to handle missing in templates
            metadata[f]['contact'] = None
    bootcamps.sort(lambda x, y: cmp(x['slug'], y['slug']))
    return bootcamps

#----------------------------------------

def harvest_single(filename):
    '''Harvest metadata from a single file.'''

    with open(filename, 'r') as reader:
        text = reader.read()
        stuff = text.split('---')[1]
        meta_dict = yaml.load(stuff)
        meta_dict['path'] = filename
        return meta_dict

#----------------------------------------

def load_info(folder):
    '''Load metadata info file from specified directory and return content.'''
    path = join(folder, INFO_YML)
    assert os.path.isfile(path), \
           'No info file found in folder "{0}"'.format(folder)
    with open(path, 'r') as reader:
        return yaml.load(reader)

#----------------------------------------

def prev_next(this, ordered, lookup):
    '''
    Return prev and next links.  `ordered` must be a list of path
    names in order; `lookup` must be a dictionary mapping path names
    to their indices in that list.  We can't simply build the latter
    here because it sometimes requires flattening of nested lists to
    construct (when the files in question comes from
    sub-sub-directories).
    '''
    assert len(ordered) == len(lookup), \
           'Lookup table and ordered list length mis-match'
    prev = next = None
    this_i = lookup[this]
    if this_i > 0:
        prev = ordered[this_i - 1]
    if this_i < len(ordered)-1:
        next = ordered[this_i + 1]
    return prev, next

#----------------------------------------

def render(options, src, root, page):
    '''
    Render the template file `src` using the page settings provided
    and the global settings.  The output filename is constructed by
    concatenating the output directory name and the source filename.
    `root` is used as the relative path to the root of the web site.
    '''
    dst = join(options.output, src)
    template = options.env.get_template(src)
    site = options.site.copy()
    page['root'] = root
    page['shared'] = os.path.join(root, 'bc')
    ensure_folder(dst)
    with open(dst, 'w') as writer:
        full = template.render(site=site, page=page)
        _, _, content = full.split('---', 2)
        content = content.strip()
        writer.write(content)
        return content

#============================================================

if __name__ == '__main__':
    main()
