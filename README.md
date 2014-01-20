Software Carpentry Web Site
===========================

This repository holds the source for
the [Software Carpentry](http://software-carpentry.org) web site.
Home pages for bootcamps are not stored in this repository:
if you want to create one,
please see the instructions in the [`bc` repository](https://github.com/swcarpentry/bc).

Contributing
------------

Software Carpentry is an open source/open access project,
and we welcome contributions of all kinds.
By contributing,
you are agreeing that Software Carpentry may redistribute your work
under [these licenses](http://software-carpentry.org/license.html).

Software Carpentry uses a development workflow similar to that of [AstroPy](http://astropy.org)
and many other open source projects.
The AstroPy docs have excellent sections on:

*   [Getting started with Git](http://astropy.readthedocs.org/en/latest/development/workflow/index.html#getting-started-with-git)
*   [Developer workflow](http://astropy.readthedocs.org/en/latest/development/workflow/development_workflow.html)

Cloning
-------

To build this web site,
you will need to clone `git@github.com:swcarpentry/site.git`,
and then clone the submodule `https://github.com/swcarpentry/v4.git`.

Note: this repository takes up roughly 360 MBytes
(including what's in `.git`),
and the Version 4 lesson materials add another 300 MBytes.

Building
--------

Building the web site requires: 

*   [Jekyll](http://jekyllrb.com/), used to compile templated HTML pages
*   [Python](http://python.org/), used for pre- and post-processing

Python packages can be installed using:

~~~
$ pip install -r requirements.txt
~~~

We use Jekyll because it's what [GitHub](http://github.com/) uses;
we use Python because most of our volunteers speak it.

*   Type `make` to see a list of all available commands.
*   Type `make cache` to fetch information about upcoming bootcamps.
    This must be done before building the web site.
*   Type `make check` to build everything in `_site` for testing.
    (Depending on your machine, this takes about 10-15 seconds.)

We try to use the same MarkDown interpreters as GitHub does for
consistency.  On OS X, we suggest you use a recent Ruby to get access
to these.  If you don't have Homebrew or MacPorts installed, here's a
quick recipe to get started using HomeBrew.

~~~
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
brew install ruby
gem install jekyll
gem install RedCloth
~~~

Design Notes
------------

*   We generate our own RSS feed (in `feed.xml`) and blog home page
    because Jekyll insists on using `_posts/YYYY-MM-DD-name.html`,
    and we don't want to have hundreds of files in one directory.
*   Bootcamp pages for old bootcamps
    are stored in the `bootcamps` directory of this repository,
    since there's little point in creating repos for them.
    New bootcamps should be created using the process described below.

Adding Bootcamps
----------------

Old bootcamps' home pages are stored in `bootcamps/yyyy-mm-dd-site/index.html`.
Newer bootcamps' home pages are stored in their own repositories on GitHub.
The make target `make cache` runs the program `bin/get_bootcamp_info.py`
which reads a list of GitHub repository URLs from the file `config/bootcamp_urls.yml`
and (re-)creates the file `./_bootcamp_cache.yml`.
That file is then used to build `./index.html`, `bootcamps/index.html`, and so on.
To add another GitHub-hosted bootcamp to this web site,
simply add a line to `config/bootcamp_urls.yml`.
Please keep these ordered by date.

Blogging 
--------

To create a new blog post:

1.  Fork this repository on GitHub, and clone that to your desktop.
2.  Create a file `blog/YYYY/MM/post-name.html`,
    where `YYYY` is a four-digit year and `MM` is a two-digit month.
3.  Fill in the metadata at the top of the file:
    *   `layout` *must* be `blog`.
    *   `author` must be the author's name.  (It does not need to be quoted.)
    *   `title` is the post title.
    *   `date` the date of the post (in YYYY-MM-DD format).
    *   `time` must be an HH:MM:TT clock time.
        Use 09:00:00 for the first post on a particular day,
        10:00:00 for the second,
        and so on,
        so that posts can be ordered.
    *   `category` must be a list of category identifiers, e.g.,
        `["Euphoric State University", "Assessment"]`
        You can run the command `make categories` to get a list of existing category names.
4.  Use HTML to write the post.
    *   Use `<!-- start excerpt -->` and `<!-- end excerpt -->`
        to mark a paragraph or two at the start
        as the excerpt to show in feed readers.
    *   If you need to refer to our email address, it is `{{page.contact}}`.
    *   If you need to another post, or something else on the site, use `{{page.root}}/path/to/file`.
    *   We also provide `{{site.site}}` (the base URL for the site),
        `{{site.twitter_name}}`,
        `{{site.twitter_url}}`,
        `{{site.facebook_url}}`,
        `{{site.google_plus_url}}`,
        and `{{site.rss_url}}`
        (all of which should be self-explanatory),
        and `{{site.msl_url}}` for the Mozilla Science Lab's web site.
5.  Please add any images your blog post needs to the same blog/YYYY/MM directory as the post itself.
    Please use lower-case names without special characters for image files.
6.  `make` in the root directory will list available commands;
    `make check` will rebuild the web site in the `_site` directory.
    Open `_site/index.html` to see your post on the blog's home page,
    `_site/blog/index.html` to see it on the blog home page,
    and `_site/YYYY/MM/post-name.html` to see the post itself.
7.  When you're satisfied with your post,
    `git add path/to/post` and `git commit -m "Adding a blog post about something or other"`
    will commit it to your local copy (on your laptop).
8.  `git push origin master` will push it to your clone on GitHub
    (assuming you've added your fork on GitHub as a remote called `origin`).
9.  Go to GitHub and issue a pull request from your clone to `swcarpentry/website`,
    then assign it to `@gvwilson` or `@amyrbrown` for proof-reading.

Available Commands
------------------

*   `authors`: list all blog post authors.
*   `biblio`: make HTML and PDF of bibliography.
*   `cache_verb` : collect bootcamp information from GitHub and store in local cache (verbose).
*   `cache`: collect bootcamp information from GitHub and store in local cache.
*   `categories : list all blog category names.
*   `check`: build locally into _site directory for checking.
*   `clean`: clean up.
*   _`commands`_: show all commands (the default).
*   `dev`: build into development directory on server.
*   `install`: build into installation directory on server.
*   `links`: check links.
*   `sterile`: *really* clean up.
*   `valid`: check validity of HTML.

The Details
-----------

`make check`, `make dev`, and `make install` do the following:

1.  Run `bin/preprocess.py` to create the `./_config.yml` file required by Jekyll
    and the `_includes/recent_blog_posts.html` file containing excerpts of recent blog posts.
    This tool collects metadata about blog posts and bootcamps
    and combines it with static configuration information.
2.  Run Jekyll to build the web site.
3.  Run `bin/make_rss_feed.py` to generate the RSS feed file `feed.xml`.
4.  Run `bin/make_calendar.py` to generate the ICal calendar file `bootcamps.ics`.
5.  Copy `./_htaccess` to create the `.htaccess` file for the web site.

Badges
------

Software Carpentry uses [Open Badges](http://openbadges.org/) to recognize people's skills and accomplishments.
To create badges, you must install [PyPNG](http://pythonhosted.org/pypng/index.html) module:

~~~
$ pip install pypng
~~~

Use `bin/badge-create.py` to create a new badge:

~~~
$ python bin/badge-create.py --username abbrev.name --email name@site.com --kind instructor
~~~

The badges scripts in `bin` should be compatible with Python2 and Python3.
To bake the badge we use `bin/badgebakery.py` which was provided by the Open Badge Team.

To validate a badge:

*   Build this repository.
*   Setup a local copy of 
    [Open Badges Validator](https://github.com/mozilla/openbadges-validator-service.git).
*   Setup a virtual server that responde to http://software-carpentry.org with the
    content of `_site`.
*   Add "127.0.1.1 software-carpentry.org localhost" to `/etc/hosts`.
*   Open your local copy of Open Badges Validator with a web browser and follow the steps.
