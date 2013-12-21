Software Carpentry Badges
=========================

Software Carpentry uses [Open Badges](http://openbadges.org/) to recognize the
skills you learn.

Requirements
------------

You will need the [PyPNG](http://pythonhosted.org/pypng/index.html) module.
Install it using:

    $ pip install pypng

Create Badges
-------------

To create a new badge take a look at `bin/badge-create.py`.

Update Badges
-------------

To update a v0.5.0 badge take a look at `bin/badge-update.py`.

Developers
----------

The badges scripts in `bin` should be compatible with Python2 and Python3.

Some definitions go into `bin/badge.py` that is imported in
`bin/badge-create.py` and `bin/badge-update.py`.

To bake the badge we use `bin/badgebakery.py` that was provided by the Open
Badge Team.

To verify the badge validation:

* Build this repository
* Setup a local copy of 
  [Open Badges Validator](https://github.com/mozilla/openbadges-validator-service.git)
* Setup a virtual server that responde to http://software-carpentry.org with the
  content of `_site`
* Add "127.0.1.1    software-carpentry.org localhost" into `/etc/hosts`
* Open your local copy of Open Badges Validator with a web browser and follow
  the steps

