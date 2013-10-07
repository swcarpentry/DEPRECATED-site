#!/usr/bin/env python
'''Create a JSON blob for a badge.'''

import sys
import os
import datetime
import hashlib
import json
from PIL import Image, PngImagePlugin

#-------------------------------------------------------------------------------

BADGE_DESCRIPTIONS = {
    'core'       : ['Core Skills',
                    'Unix shell, version control, programming, and testing'],
    'instructor' : ['Instructor',
                    'Teaching at workshops or online'],
    'organizer'  : ['Organizer',
                    'Organizing workshops and learning groups'],
    'creator'    : ['Creator',
                    'Creating learning materials and other content']
}

BADGE_KINDS = BADGE_DESCRIPTIONS.keys()

USAGE = '''Usage: %(name)s username email %(kinds)s [site_dir]''' % \
{'name' : sys.argv[0], 'kinds' : '|'.join(BADGE_KINDS)}

SALT = 'software-carpentry'

#-------------------------------------------------------------------------------

def main(args):
    '''Main program driver.'''

    if (len(sys.argv) < 4) or (len(sys.argv) > 5):
        usage()

    username = sys.argv[1]
    email = sys.argv[2] 
    kind = sys.argv[3]
    website_dir = os.curdir
    if len(sys.argv) == 5:
        website_dir = sys.argv[4]

    image_src_dir = os.path.join(website_dir, 'img', 'badges')
    badge_dst_dir = os.path.join(website_dir, 'badges')

    create(image_src_dir, badge_dst_dir, kind, username, email)

#-------------------------------------------------------------------------------

def usage():
    print USAGE;
    sys.exit(-1)

#-------------------------------------------------------------------------------

def create(image_src_dir, badge_dst_dir, kind, username, email):
    '''Create JSON and PNG for a new badge.'''

    # Paths
    image_src_path, image_dst_path, json_dst_path = \
        make_paths(image_src_dir, badge_dst_dir, kind, username)

    # When is the badge being created?
    when = datetime.date.today().isoformat()

    # Hide the email address
    hashedemail = hash_email_address(email, SALT)

    # Consistent slug combining kind and username.
    slug = '%s-%s' % (kind, username)

    # Cache a few values.
    name = BADGE_DESCRIPTIONS[kind][0]
    description = BADGE_DESCRIPTIONS[kind][1]
    criteria = '/badges/index.html#%s.html' % kind
    assertion_url = '/badges/%s.json' % slug
    image_url = '/badges/%s.png' % slug

    assertion = {
        'recipient' : hashedemail,
        'salt'      : SALT,
        'issued_on' : when,
        'badge' : {
            'version'     : '0.5.0',
            'name'        : name,
            'image'       : image_url,
            'description' : description,
            'criteria'    : criteria,
            'issuer' : {
                'origin'  : 'http://software-carpentry.org',
                'name'    : 'Software Carpentry',
                'contact' : 'admin@software-carpentry.org'
            }
        }
    }

    # Create and save the JSON assertion.
    with open(json_dst_path, 'w') as writer:
        json.dump(assertion, writer, indent=4)

    # Create and save the PNG image with embedded metadata.
    img = Image.open(image_src_path)
    meta = PngImagePlugin.PngInfo()
    meta.add_text('openbadges', assertion_url)
    img.save(image_dst_path, 'PNG', pnginfo=meta)

#-------------------------------------------------------------------------------

def make_paths(image_src_dir, badge_dst_dir, kind, username):
    '''Create, check, and return the paths used by handlers.'''

    # Badge type is recognized.
    assert kind in BADGE_DESCRIPTIONS, \
           'Unknown kind of badge "%s"' % kind

    # Output directory.
    assert badge_dst_dir, \
           'Badge sub-directory not provided'
    assert os.path.isdir(badge_dst_dir), \
           'Badge destination directory "%s" does not exist' % badge_dst_dir

    # Badge image source.
    assert os.path.isdir(image_src_dir), \
           'Image source directory "%s" not found' % image_src_dir
    image_src_path = os.path.join(image_src_dir, '%s.png' % kind)
    assert os.path.isfile(image_src_path), \
           'No such image file "%s"' % image_src_path

    # Badge image destination.
    image_dst_path = os.path.join(badge_dst_dir, '%s-%s.png' % (kind, username))
    assert not os.path.isfile(image_dst_path), \
           'Output image "%s" already exists' % image_dst_path

    # JSON file.
    json_dst_path = os.path.join(badge_dst_dir, '%s-%s.json' % (kind, username))
    assert not os.path.isfile(json_dst_path), \
           'JSON file "%s" already exists' % json_dst_path

    # Report.
    return image_src_path, image_dst_path, json_dst_path

#-------------------------------------------------------------------------------

def hash_email_address(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest();

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
