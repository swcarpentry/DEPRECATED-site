Software Carpentry Website
==========================

This repository holds the source for
the [Software Carpentry](http://software-carpentry.org) website.

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

* [Getting started with Git](http://astropy.readthedocs.org/en/latest/development/workflow/index.html#getting-started-with-git)
* [Developer workflow](http://astropy.readthedocs.org/en/latest/development/workflow/development_workflow.html)

Building
--------

Building the website requires [Jekyll](http://jekyllrb.com/),
which we use to compile templated HTML pages,
and [Python](http://python.org/),
which we use for pre- and post-processing.
We use Jekyll because it's what [GitHub](http://github.com/) uses;
we use Python because most of our volunteers speak it.

* Type `make` to see a list of all available commands.
* Type `make check` to build everything in `_site` for testing.

Blogging 
--------

To create a new blog post:

1. Fork this repository on GitHub, and clone that to your desktop.
2. Create a file `blog/YYYY/MM/post-name.html`,
   where `YYYY` is a four-digit year and `MM` is a two-digit month.
3. Fill in the metadata at the top of the file:
  - `layout` *must* be `blog`.
  - `author` must be an author identifier like `wilson.g`.
    See `standard_config.yml` in repo's root directory for a list of author names
    (and add yourself if you are not there).
  - `title` is the post title.
  - `date` the date of the post (in YYYY-MM-DD format).
  - `time` must be an HH:MM:TT clock time.
    Use 09:00:00 for the first post on a particular day,
    10:00:00 for the second,
    and so on,
    so that posts can be ordered.
  - `category` must be a list of category identifiers.
    See `standard_config.yml` in repo's root directory for a list of categories
    (and add yourself if you are not there).
4. Use HTML to write the post.
   - Use `<!-- start excerpt -->` and `<!-- end excerpt -->`
     to mark a paragraph or two at the start
     as the excerpt to show in feed readers.
  - If you need to refer to our email address, it is `{{page.contact}}`.
  - If you need to another post, or something else on the site, use `{{page.root}}/path/to/file`.
  - We also provide `{{site.site}}` (the base URL for the site),
    `{{site.twitter_name}}`,
    `{{site.twitter_url}}`,
    `{{site.facebook_url}}`,
    `{{site.google_plus_url}}`,
    and `{{site.rss_url}}`
    (all of which should be self-explanatory).
5. `make` in the root directory will list available commands;
   `make check` will rebuild the web site in the `_site` directory.
   Open `_site/index.html` to see your post on the blog's home page,
   and `_site/YYYY/MM/post-name.html` to see the post itself.
6. When you're satisfied with your post,
   `git add path/to/post` and `git commit -m "Adding a blog post about something or other"`
   will commit it to your local copy (on your laptop).
7. `git push origin master` will push it to your clone on GitHub
   (assuming you've added your fork on GitHub as a remote called `origin`).
8. Go to GitHub and issue a pull request from your clone to `swcarpentry/website`,
   then assign it to `@gvwilson` or `@amyrbrown` for proof-reading.

Bootcamps
---------

Information pages for particular bootcamps are not stored in this repository:
instead,
each one has its own repository.
Setting these up is slightly complicated
because GitHub will only allow a particular user to have one fork of a particular repository.
To create a bootcamp's repository,
the bootcamp's lead instructor should do the following:

1. Create a brand new repository on GitHub for the bootcamp
   named `yyyy-mm-dd-site`,
   where `yyyy-mm-dd` is the start date for the bootcamp,
   and `site` is a site name provided by the Software Carpentry admins
   (e.g., `2015-07-03-esu`).
2. Send the URL for this repository to the Software Carpentry administrators.
3. Clone that repo to your desktop using
   `git clone https://github.com/your_user_id/yyyy-mm-dd-site`.
4. Create a `gh-pages` branch in this clone.
   (GitHub will automatically render content in this branch).
5. Add the GitHub `bootcamp` template repository as a remote by running
   `git remote add upstream https://github.com/swcarpentry/bootcamp.git`.
6. Download standard content using
   `git pull upstream gh-pages`.
7. Fill in the metadata header of `index.html`:
   - `layout` *must* be `bootcamp`.
   - `venue` is the name of the institution or group hosting the bootcamp.
   - `address` is the bootcamp venue's street address.
   - `latlng` is the latitude and longitude of the bootcamp site
     (so we can put a pin on our map).
   - `humandate` is the human-friendly dates for the bootcamp (e.g., July 3-4, 2015).
   - `startdate` is the bootcamp's starting date in YYYY-MM-DD format.
   - `enddate` is the bootcamp's ending date in the same format.
   - `registration` is `open` (if anyone is allowed to sign up)
     or `restricted` (if only some people are allowed to take part).
   - `instructor` is a comma-separated list of instructor names.
     This *must* be enclosed in square brackets, as in
     `["Alan Turing", "Grace Hopper"]`.
8. Edit the page to describe what you'll be covering,
   to include stock lesson material,
   etc.
   Please use the includable files in the `_includes` directory
   whenever you can.
9. Commit your changes locally,
   then push them to the `gh-pages` branch of your GitHub repository using:
   `git push origin gh-pages`.
   Note that you push to *origin*, not to *upstream*:
   you should not have permission to change the latter.

Note: if you are using Git and GitHub in your class,
you may use the `master` branch of your `yyyy-mm-dd-site` repository for student work,
or you may create another repository
(with any name you want)
for students to use.
The former is more economical;
the latter is safer.

If you wish to send improvements and additions back to the master copy of `bootcamp`:

1. Fork `bootcamp` on GitHub and clone that to your desktop.
2. Add your desktop `yyyy-mm-dd-site` repository as a remote.
3. Push changes from `yyyy-mm-dd-site` to `bootcamp` on your desktop.
4. Push those to your GitHub fork of `bootcamp` and issue a PR as usual.

Once again,
this slightly circuitous procedure is needed because
GitHub only allows a particular user to have one fork of a repo at once,
and instructors frequently need to work on several bootcamps simultaneously.

Design Notes
------------

* The material in the `_includes` directory
  is duplicated in the `bootcamp` template repository.
  We could create a third repository for this,
  and make it a submodule of the two main ones,
  but our experience with submodules hasn't been positive.
* We generate our own RSS feed (in `feed.xml`) and blog home page
  because we don't want to break existing URLs:
  Jekyll insists on using `_posts/YYYY-MM-DD-name.html`,
  while the posts we're importing are all `YYYY/MM/DD/name.html`.
  We could use HTTP redirects to translate one into the other,
  but (a) that would still leave us with hundreds of files in a single directory,
  and (b) developers would then have to run a local server with the right `.htaccess`
  to view posts in progress.
* Bootcamp pages for old bootcamps
  are stored in the `bootcamps` directory of this repository,
  since there's little point in creating repos for them.
  New bootcamps should be created using the process described earlier.
