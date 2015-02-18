import sys
import re
from get_workshop_info import fetch, check_info

assert len(sys.argv) == 2, 'Usage: check_workshop.py url'
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
