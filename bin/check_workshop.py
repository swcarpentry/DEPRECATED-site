import sys
from get_workshop_info import fetch, check_info

assert len(sys.argv) == 2, 'Usage: check_workshop.py url'
url = sys.argv[1]

info = fetch(url)
info['url'] = url
if check_info(url, info):
    print 'OK'
else:
    print 'failure'
