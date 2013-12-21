"""Utility library for Software Carpentry badges"""

SALT = "software-carpentry"
URL = "http://software-carpentry.org"

BADGE_DESCRIPTIONS = {
    "core"       : ["Core Skills",
                    "Unix shell, version control, programming, and testing"],
    "creator"    : ["Creator",
                    "Creating learning materials and other content"],
    "helper"     : ["Helper",
                    "Helping at workshops or online"],
    "instructor" : ["Instructor",
                    "Teaching at workshops or online"],
    "organizer"  : ["Organizer",
                    "Organizing workshops and learning groups"]
}

BADGE_KINDS = BADGE_DESCRIPTIONS.keys()

def set_verify_url(class_name, username):
    assert class_name in BADGE_KINDS, \
            "Can't match badge.name field."
    return "{0}/badges/{1}/{2}.json".format(
            URL, class_name.lower(), username)

def set_badge_url(class_name):
    assert class_name in BADGE_KINDS, \
            "Can't match badge.name field."
    return "{0}/badges/class/{1}.json".format(
            URL, class_name.lower())

def set_image_url(class_name):
    assert class_name in BADGE_KINDS, \
            "Can't match badge.name field."
    return "{0}/img/badges/{1}.png".format(
            URL, class_name.lower())
