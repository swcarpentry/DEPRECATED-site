#!/usr/bin/env python
'''Check the index.html data of a workshop given its URL.'''

import sys
import re
from workshops import fetch, check_info

assert len(sys.argv) == 2, 'Usage: url-check.py url'
url = sys.argv[1]

m = re.match(r'^https?://(.+)\.github\.io/([^/]+)/?$', url)
if m:
    url = 'https://github.com/{0}/{1}'.format(m.group(1), m.group(2))

info = fetch(url)
info['url'] = url
if check_info(url, info):
    print url
else:
    print 'FAIL:', url
