"""
Download information about bootcamps from GitHub.
Usage: get_bootcamp_info [-i input_file] [-o output_file] [-t]
-i: optional input filename (default sys.stdin)
-o: optional output filename (default sys.stdout)
-t: tolerate errors (default False)
If the -t flag is used, output is written for all correct entries.
If it is not, output is only written if *all* entries are correct.
"""

import sys
import re
import datetime
from optparse import OptionParser
import yaml
import requests

GITHUB_IO_TEMPLATE = 'http://{0}.github.io/{1}/'

GITHUB_URL_RE = re.compile(r'^https?://github\.com/([^/]+)/([^/]+)')

REQUIRED_KEYS = set('country humandate startdate url venue'.split())

LATLNG_RE = re.compile(r'\s*-?\d+(\.\d*)?,\s*-?\d+(\.\d*)?\s*')

ARCHIVE_WINDOW = 3

def _cleanup_handler(record, key, value):
    if ((type(value) == str) and LATLNG_RE.match(value)):
        return value
    else:
        print >> sys.stderr, 'Bad field in "{0}" for key "{1}": "{2}"'.format(record, key, value)
        return None
CLEANUP = {
    'latlng' : _cleanup_handler
}

def main(args):
    '''Main driver.'''

    reader_filename, writer_filename, archiver_filename, tolerate, verbose = setup(args)

    reader, writer = sys.stdin, sys.stdout
    if reader_filename != '-':
        reader = open(reader_filename, 'r')
    if writer_filename != '-':
        # We append due the way that we call this script in `Makefile`.
        writer = open(writer_filename, 'a')

    all_urls = yaml.load(reader)
    reader.close()

    results, faulty = process(all_urls, verbose)
    if faulty:
        print >> sys.stderr, 'Errors in these URLs:'
        for f in faulty:
            print >> sys.stderr, '  {0}'.format(f)
    elif archiver_filename:
        reader = open(reader_filename, 'w')
        archiver = open(archiver_filename, 'a')
        archive(all_urls, results, reader, archiver)
        reader.close()
        archiver.close()

    if (not faulty) or tolerate:
        cleanup(results)
        yaml.dump(results, writer)

    writer.close()

def setup(args):
    '''Parse command-line arguments and return input and output streams.'''
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', help='input file', default='-')
    parser.add_option('-o', '--output', dest='output', help='output file', default='-')
    parser.add_option('--archive', dest='archive', help='archive file', default=None)
    parser.add_option('-t', '--tolerate', dest='tolerate', help='tolerate errors',
                      default=False, action='store_true')
    parser.add_option('-v', '--verbose', dest='verbose', help='report progress',
                      default=False, action='store_true')
    options, args = parser.parse_args(args)

    return options.input, options.output, options.archive, options.tolerate, options.verbose

def process(all_urls, verbose):
    '''
    Process URLs, returning list of valid info structures and list
    of URLs found faulty.
    '''
    results = []
    faulty = []
    for url in all_urls:
        info = fetch(url)
        info['user'], info['slug'] = extract_info_from_url(url)
        info['url'] = GITHUB_IO_TEMPLATE.format(info['user'], info['slug'])
        if check_info(url, info):
            if verbose:
                print '+', url
            results.append(info)
        else:
            if verbose:
                print '!', url
            faulty.append(url)
    return results, faulty

def fetch(url):
    '''Fetch information from a single online repository.'''
    url = url.replace('github.com', 'raw.github.com') + '/gh-pages/index.html'
    response = requests.get(url)
    if response.status_code != 200:
        fail('Request for {0} returned status code {1}', url, response.status_code)
    pieces = response.text.split('---')
    if len(pieces) < 2:
        fail('Malformed YAML header in {0}', url)
    info = yaml.load(pieces[1])
    return info

def extract_info_from_url(url):
    '''Extract username and project name from GitHub URL.'''
    match = GITHUB_URL_RE.search(url)
    if not match:
        print >> sys.stderr, 'URL {0} does not match pattern'.format(url)
        sys.exit(1)
    user = match.group(1)
    slug = match.group(2)
    if (not user) or (not slug):
        print >> sys.stderr, 'URL {0} has empty user and/or slug'.format(url)
        sys.exit(1)
    return user, slug

def check_info(url, info):
    '''Check that all required information for bootcamp is present.'''
    missing = REQUIRED_KEYS - set(info.keys())
    if missing:
        missing = sorted(list(missing))
        print >> sys.stderr, 'Info for {0} missing key(s): {1}'.format(url, missing)
        return False
    return True

def cleanup(entries):
    '''Sanitize entries (e.g., convert 'TBD' to none).'''
    for entry in entries:
        for key in CLEANUP:
            if key in entry:
                entry[key] = CLEANUP[key](entry, key, entry[key])

def fail(template, *args):
    '''Format and print error message, then exit.'''
    msg = template.format(*args)
    print >> sys.stderr, msg
    sys.exit(1)

def archive(all_urls, results, reader, archiver):
    upcoming_urls = []
    archive_info = []

    # Have to loop over the positions to sync all_urls and results
    for i in range(len(all_urls)):
        end_url = all_urls[i].split('/')[-1]
        # Check sync between all_urls and results
        if end_url == results[i]['slug']:
            if should_be_archived(results[i]):
                archive_info.append(results[i])
            else:
                upcoming_urls.append(all_urls[i])
        else:
            upcoming_urls.append(all_urls[i])

    yaml.dump(upcoming_urls, reader, default_flow_style=False)
    if archive_info:
        yaml.dump(archive_info, archiver)

def should_be_archived(record):
    if 'enddate' in record:
        checkdate = record['enddate']
    else:
        checkdate = record['startdate']
    return (datetime.date.today() - checkdate) > datetime.timedelta(ARCHIVE_WINDOW)

if __name__ == '__main__':
    main(sys.argv[1:])
