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
import badge
import badgebakery

def main(badge_filename, save_result, baking, backups):
    """Main program driver."""
    with open(badge_filename, "r") as f:
        badge = json.load(f)

    # Check if badge is from the older API
    if type(badge["badge"]) is dict:
        badge_name = badge["badge"]["name"]
        badge = update_badge_assertion(badge, badge_filename)
        output = json.dumps(badge, indent=True, sort_keys=True)
        if not save_result and not baking:
            print(output)
        else:
            if backups:
                shutil.copyfile(badge_filename, "{}.bak".format(badge_filename))
            with open(badge_filename, "w") as f:
                f.write(output)
            if baking:
                badgebakery.bake_badge('img/badges/{0}.png'.format(badge_name.lower()),
                        badge_filename.replace('.json', '.png'),
                        badge_filename)
    else:
        print("Badge already on version 1.0.0")

def update_badge_assertion(old_badge, badge_filename):
    """Create a BadgeAssertion based on the old badge structure.

    For more information about BadgeAssertion:
    https://github.com/mozilla/openbadges-specification/blob/master/Assertion/latest.md#structures.
    """
    new_badge = {
        "uid":old_badge["recipient"],
        "recipient":{
            "identity":old_badge["recipient"],
            "type":"email",
            "hashed":True},
        "badge":badge.set_badge_url(old_badge["badge"]["name"].lower()),
        "verify":{
            "type":"hosted",
            "url":"{0}/{1}".format(badge.URL, badge_filename)}}

    if "salt" in old_badge:
        new_badge["recipient"]["salt"] = old_badge["salt"]
    if "issued_on" in old_badge:
        new_badge["issuedOn"] = old_badge["issued_on"]

    if "badge" in old_badge and "image" in old_badge["badge"]:
        # Check for relative path
        if old_badge["badge"]["image"][0] == "/":
            new_badge["image"] = "{0}{1}".format(
                    badge.URL, old_badge["badge"]["image"])
        else:
            new_badge["image"] = old_badge["badge"]["image"]
    else:
        new_badge["image"] = set_image_url(old_badge["badge"]["name"])

    if "evidence" in old_badge:
        new_badge["evidence"] = old_badge["evidence"]

    if "expires" in old_badge:
        new_badge["expires"] = old_badge["expires"]

    return new_badge

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
            description="A python script to update a JSON blob for a badge from v0.5.0 to v1.0.0")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("-w", "--write", action="store_true",
            help="Write back modified badge")
    action.add_argument("-b", "--baking", action="store_true",
            help="Write back modified badge and bake it")
    parser.add_argument("--backups", action="store_true",
            help="Write backups for modified badges")
    parser.add_argument("badge", nargs="+",
            help="The name of the JSON blob to update")

    args = parser.parse_args()

    for b in args.badge:
        main(b, args.write, args.baking, args.backups)
