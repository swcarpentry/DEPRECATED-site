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
    ('swcarpentry/capstone-novice-spreadsheet-biblio', 'From Excel to a database via Python'),
    ('swcarpentry/instructor-training', 'What instructors need to know'),
    ('swcarpentry/python-novice-turtles', 'Python for non-programmers using Turtles'),
    ('swcarpentry/amy', 'Workshop administration tool'),
    ('swcarpentry/site', 'Software Carpentry website'),
)

g = Github()
all_records = []
dashboard = {
    'records' : all_records,
    'num_repos' : 0,
    'num_issues' : 0,
    'num_pulls' : 0
}
for (ident, description) in controls:
    dashboard['num_repos'] += 1
    r = g.get_repo(ident)
    record = {'ident' : ident,
              'description' : description,
              'url' : r.html_url,
              'issues' : [],
              'pulls' : []}
    all_records.append(record)
    for i in r.get_issues(state='open'):
        record['issues'].append({'number' : i.number,
                                 'title' : i.title,
                                 'url' : i.html_url})
        dashboard['num_issues'] += 1
    for p in r.get_pulls(state='open'):
        record['pulls'].append({'number' : p.number,
                                'title' : p.title,
                                'url' : p.html_url})
        dashboard['num_pulls'] += 1

yaml.dump(dashboard, sys.stdout, encoding='utf-8', allow_unicode=True)
