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
from optparse import OptionParser
import yaml
import requests

GITHUB_IO_TEMPLATE = 'http://{0}.github.io/{1}/'

GITHUB_URL_RE = re.compile(r'^https?://github\.com/([^/]+)/([^/]+)')

REQUIRED_KEYS = set('country humandate startdate url venue'.split())

LATLNG_RE = re.compile(r'\s*-?\d+(\.\d*)?,\s*-?\d+(\.\d*)?\s*')

CLEANUP = {
    'latlng' : lambda(s): s if LATLNG_RE.match(s) else None
}

def main(args):
    '''Main driver.'''

    reader, writer, tolerate, verbose = setup(args)
    all_urls = yaml.load(reader)

    results, faulty = process(all_urls, verbose)
    if faulty:
        print >> sys.stderr, 'Errors in these URLs:'
        for f in faulty:
            print >> sys.stderr, '  {0}'.format(f)

    if (not faulty) or tolerate:
        cleanup(results)
        yaml.dump(results, writer)

    reader.close()
    writer.close()

def setup(args):
    '''Parse command-line arguments and return input and output streams.'''
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', help='input file', default='-')
    parser.add_option('-o', '--output', dest='output', help='output file', default='-')
    parser.add_option('-t', '--tolerate', dest='tolerate', help='tolerate errors',
                      default=False, action='store_true')
    parser.add_option('-v', '--verbose', dest='verbose', help='report progress',
                      default=False, action='store_true')
    options, args = parser.parse_args(args)

    reader, writer = sys.stdin, sys.stdout
    if options.input != '-':
        reader = open(options.input, 'r')
    if options.output != '-':
        writer = open(options.output, 'w')

    return reader, writer, options.tolerate, options.verbose

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
    for e in entries:
        for k in CLEANUP:
            if k in e:
                e[k] = CLEANUP[k](e[k])

def fail(template, *args):
    '''Format and print error message, then exit.'''
    msg = template.format(*args)
    print >> sys.stderr, msg
    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
