#!/usr/bin/env python
'''Update a JSON blob for a badge from v0.5.0 to v1.0.0. Change information can
be found at
https://github.com/mozilla/openbadges/wiki/Assertion-Specification-Changes.'''

import sys
import os
import shutil
import datetime
import hashlib
import json

def main(fbadge, write, nobackups):
    '''Main program driver.'''
    badge = read_old(fbadge)
    badge['file-name'] = fbadge  # We need the name of the file.
    badge = create_badge_assertion(badge)
    output = json.dumps(badge, indent=True, sort_keys=True)
    if not write and not nobackups:
        print(output)
    else:
        if write:
            shutil.copyfile(fbadge, '{}.bak'.format(fbadge))
        with open(fbadge, 'w') as f:
            f.write(output)

def read_old(fbadge):
    """Read JSON with old badge."""
    with open(fbadge, 'r') as f:
        badge = json.load(f)
    return badge

def create_badge_assertion(old_badge):
    """Create a BadgeAssertion based on the old badge structure.

    For more information about BadgeAssertion:
    https://github.com/mozilla/openbadges-specification/blob/master/Assertion/latest.md#structures.

    NOTE: for non-mandatory fields we use a `try` block.
    """
    new_badge = dict()

    new_badge['uid'] = old_badge['recipient']

    new_badge['recipient'] = dict()
    new_badge['recipient']['identity'] = old_badge['recipient']
    new_badge['recipient']['type'] = 'hosted'
    new_badge['recipient']['hashed'] = True
    try:
        new_badge['recipient']['salt'] = old_badge['salt']
    except:
        pass

    if old_badge['badge']['name'] == 'Creator':
        new_badge['badge'] = 'http://software-carpentry.org/badges/class/creator.json'
    elif old_badge['badge']['name'] == 'Instructor':
        new_badge['badge'] = 'http://software-carpentry.org/badges/class/instructor.json'
    elif old_badge['badge']['name'] == 'Organizer':
        new_badge['badge'] = 'http://software-carpentry.org/badges/class/organizer.json'
    else:
        raise ValueError('Can\'t match badge.name field.')

    new_badge['verify'] = dict()
    new_badge['verify']['type'] = 'hosted'
    new_badge['verify']['url'] = 'http://software-carpentry.org/{0}'.format(
            old_badge['file-name'])

    try:
        new_badge['issuedOn'] = old_badge['issued_on']
    except:
        pass

    try:
        # Check for relative path
        if old_badge['badge']['image'][0] == '/':
            new_badge['image'] = 'http://software-carpentry.org{0}'.format(
                    old_badge['badge']['image'])
        else:
            new_badge['image'] = old_badge['badge']['image']
    except:
        if old_badge['badge']['name'] == 'Creator':
            new_badge['image'] = 'http://software-carpentry.org/img/badges/creator.png'
        elif old_badge['badge']['name'] == 'Instructor':
            new_badge['image'] = 'http://software-carpentry.org/img/badges/instructor.png'
        elif old_badge['badge']['name'] == 'Organizer':
            new_badge['badge'] = 'http://software-carpentry.org/badges/class/organizer.json'
        else:
            raise ValueError('Can\'t match badge.name field.')

    try:
        new_badge['evidence'] = old_badge['evidence']
    except:
        pass

    try:
        new_badge['expires'] = old_badge['expires']
    except:
        pass


    return new_badge

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
            description='A python script to update a JSON blob for a badge from v0.5.0 to v1.0.0')
    parser.add_argument('-w', '--write', action='store_true',
            help='Write back modified badge')
    parser.add_argument('-n', '--nobackups', action='store_true',
            help='Don\'t write backups for modified badges')
    parser.add_argument('badge', nargs='+',
            help='The name of the JSON blob to update')

    args = parser.parse_args()

    for b in args.badge:
        main(b, args.write, args.nobackups)
