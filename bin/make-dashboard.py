#!/usr/bin/env python

'''Create YAML for dashboard page by querying GitHub repositories.'''

import sys
import yaml
from github import Github
from util import DASHBOARD_CACHE

controls = (
    ('swcarpentry/shell-novice', 'Introduction to the Unix shell'),
    ('swcarpentry/git-novice', 'Introduction to Git'),
    ('swcarpentry/hg-novice', 'Introduction to Mercurial'),
    ('swcarpentry/sql-novice-survey', 'Introduction to SQL'),
    ('swcarpentry/python-novice-inflammation', 'Python for non-programmers'),
    ('swcarpentry/r-novice-inflammation', 'R for non-programmers'),
    ('swcarpentry/matlab-novice-inflammation', 'MATLAB for non-programmers'),
    ('swcarpentry/slideshows', 'Software Carpentry presentations'),
    ('swcarpentry/capstone-novice-spreadsheet-biblio', 'From Excel to a database via Python'),
    ('swcarpentry/instructor-training', 'What instructors need to know'),
    ('swcarpentry/python-novice-turtles', 'Python for non-programmers using Turtles'),
    ('swcarpentry/amy', 'Workshop administration tool'),
    ('swcarpentry/site', 'Software Carpentry website'),
)

assert len(sys.argv) == 3, 'Usage: make-dashboard.py token-file output-file'
token_file = sys.argv[1]
output_file = sys.argv[2]

with open(token_file, 'r') as reader:
    token = reader.read().strip()

g = Github(token)
all_records = []
dashboard = {
    'records' : all_records,
    'num_repos' : 0,
    'num_issues' : 0
}
for (ident, description) in controls:
    print '+', ident
    dashboard['num_repos'] += 1
    r = g.get_repo(ident)
    record = {'ident' : ident,
              'description' : description,
              'url' : str(r.html_url),
              'issues' : []}
    all_records.append(record)
    for i in r.get_issues(state='open'):
        record['issues'].append({'number' : i.number,
                                 'title' : str(i.title),
                                 'url' : str(i.html_url)})
        dashboard['num_issues'] += 1

with open(output_file, 'w') as writer:
    yaml.dump(dashboard, writer, encoding='utf-8', allow_unicode=True)
