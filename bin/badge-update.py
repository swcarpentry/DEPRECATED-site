#!/usr/bin/env python
"""Update a JSON blob for a badge from v0.5.0 to v1.0.0. Change information can
be found at
https://github.com/mozilla/openbadges/wiki/Assertion-Specification-Changes."""

import sys
import os
import shutil
import datetime
import hashlib
import json

SwCarpentryURL = "http://software-carpentry.org"

def main(badge_filename, save_result, backups):
    """Main program driver."""
    badge = read_old(badge_filename)

    # Check if badge is from the older API
    if type(badge["badge"]) is dict:
        badge = update_badge_assertion(badge, badge_filename)
        output = json.dumps(badge, indent=True, sort_keys=True)
        if not save_result and not backups:
            print(output)
        else:
            if backups:
                shutil.copyfile(badge_filename, "{}.bak".format(badge_filename))
            with open(badge_filename, "w") as f:
                f.write(output)

def read_old(badge_filename):
    """Read JSON with old badge."""
    with open(badge_filename, "r") as f:
        badge = json.load(f)
    return badge

def update_badge_assertion(old_badge, badge_filename):
    """Create a BadgeAssertion based on the old badge structure.

    For more information about BadgeAssertion:
    https://github.com/mozilla/openbadges-specification/blob/master/Assertion/latest.md#structures.

    NOTE: for non-mandatory fields we use a `try` block.
    """
    new_badge = {
        "uid":old_badge["recipient"],
        "recipient":{
            "identity":old_badge["recipient"],
            "type":"email",
            "hashed":True},
        "badge":set_badge(old_badge["badge"]["name"]),
        "verify":{
            "type":"hosted",
            "url":"{0}/{1}".format(SwCarpentryURL, badge_filename)}}

    if "salt" in old_badge.keys():
        new_badge["recipient"]["salt"] = old_badge["salt"]
    if "issued_on" in old_badge.keys():
        new_badge["issuedOn"] = old_badge["issued_on"]

    if "badge" in old_badge.keys() and "image" in old_badge["badge"].keys():
        # Check for relative path
        if old_badge["badge"]["image"][0] == "/":
            new_badge["image"] = "{0}{1}".format(
                    SwCarpentryURL, old_badge["badge"]["image"])
        else:
            new_badge["image"] = old_badge["badge"]["image"]
    else:
        new_badge["image"] = set_badge_image(old_badge["badge"]["name"])

    if "evidence" in old_badge.keys():
        new_badge["evidence"] = old_badge["evidence"]

    if "expires" in old_badge.keys():
        new_badge["expires"] = old_badge["expires"]

    return new_badge

def set_badge(name):
    assert name in ['Creator', 'Instructor', 'Organizer'], "Can't match badge.name field."
    return "{0}/badges/class/{1}.json".format(
            SwCarpentryURL, name.lower())

def set_badge_image(name):
    assert name in ['Creator', 'Instructor', 'Organizer'], "Can't match badge.name field."
    return "{0}/img/badges/{1}.json".format(
            SwCarpentryURL, name.lower())

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
            description="A python script to update a JSON blob for a badge from v0.5.0 to v1.0.0")
    parser.add_argument("-w", "--write", action="store_true",
            help="Write back modified badge")
    parser.add_argument("-b", "--backups", action="store_true",
            help="Write backups for modified badges")
    parser.add_argument("badge", nargs="+",
            help="The name of the JSON blob to update")

    args = parser.parse_args()

    for b in args.badge:
        main(b, args.write, args.backups)
