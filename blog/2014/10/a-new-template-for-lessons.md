Lesson Layout
=============

Terms
-----

A *lesson* is a complete story about some subject, typically taught in 2-4 hours.

A *topic* is a single scene in that story, typically 5-15 minutes long.

A *slug* is a short identifier for something, such as `filesys` (for "file system").

Design Choices
--------------

* We define everything in terms of Markdown.
  If lesson authors want to use something else for their lessons (e.g., IPython Notebooks),
  it's up to them to generate and commit Markdown formatted according to the rules below.

* We will use Pandoc for Markdown-to-HTML conversion,
  so we can use `{.attribute}` syntax for specifying anchors and classes
  rather than the clunky syntax our current notes use
  to be compatible with Jekyll.

* We will avoid putting HTML inside Markdown since it's ugly to read and write,
  and error-prone to process.
  As a consequence,
  we put things like the learning objectives and each challenge exercise
  in a block indented with `>`
  to make scope easier for people and machines to see.

Overall Layout
--------------

Each lesson is stored in a directory that is laid out as described below.
That directory is a self-contained Git repository
(i.e., there are no submodules or clever tricks with symbolic links).

1.  `index.md`: the home page for the lesson.
    (See "Home Page" below.)

2.  `dd-slug.md`: the topics in the lesson.
    `dd` is a sequence number such as `01`, `02`, etc.,
    and `slug` is an abbreviated single-word mnemonic for the topic.
    Thus, `03-filesys.md` is the third topic in this lesson,
    and is about the filesystem.
    (Note that we use hyphens rather than underscores in filenames.)
    See "Topics" below.

3.  `intro.md`: slides for a short presentation (3 minutes or less)
    explaining what the lesson is about and why people would want to learn it.
    See "Introductory Slides" below.

4.  `glossary.md`: definitions of key terms.
    This is what the lesson exports that other lessons can use
    (just as an API is the functions a library exports for other code to use).
    See "Glossary" below.

5.  `reference.md`: a reference guide to key terms and commands, syntax, etc.,
    to be printed and given to learners.
    See "Reference Guide" below.

6.  `instructors.md`: the instructor's guide for the lesson.
    See "Instructor's Guide" below.

7.  `code/`: a sub-directory containing all code samples.
    See "Software and Data" below.

8.  `data/`: a sub-directory containing all data files for this lesson.
    See "Software and Data" below.

9.  `img/`: images (including plots) used in the lesson.
    See "Images" below.

10. `web/`: web resources, such as CSS files, icons, and Javascript.
    See "Web Resources" below.

11. `_layouts/`: page layout templates.
    See "Web Resources" below.

12. `_includes/`: page inclusions.
    See "Web Resources" below.

13. `bin/`: tools for managing lessons.
    See "Tools" below.

14. `Makefile` contains commands to build and manage the lesson.
    (See "Tools" below.)

Home Page
---------

`index.md` must be structured as follows:

    ---
    layout: lesson
    title: Lesson Title
    keywords: ["some", "key terms", "in a list"]
    ---
    Paragraph of introductory material.

    > ## Prerequisites {.prereq}
    >
    > A short paragraph describing what learners need to know
    > before tackling this lesson.

    > ## Learning Objectives {.objectives}
    >
    > * Overall objective 1
    > * Overall objective 2

    ## Topics

    * [Topic Title 1](01-slug.html)
    * [Topic Title 2](02-slug.html)

    ## Other Resources

    * [Introduction](intro.html)
    * [Glossary](glossary.html)
    * [Reference Guide](reference.html)
    * [Instructor's Guide](guide.html)
    * [Setting Up](http://software-carpentry.org/setup/some-page.html)

**Note:** software installation and configuration instructions *aren't* in the lesson.
They may be shared with other lessons,
so they will be stored centrally on the Software Carpentry web site
and linked from the lessons that need them.

**Note:** the description of prerequisites is prose for human consumption,
not a machine-comprehensible list of dependencies.
We may supplement the former with the latter
once we have more experience with this lesson format
and know what we actually want to do.

Topics
------

Each topic must be structured as follows:

    ---
    layout: topic
    title: Topic Title
    ---
    > ## Learning Objectives {.objectives}
    >
    > * Learning objective 1
    > * Learning objective 2

    Paragraphs of text mixed with:

    ~~~ {.python}
    some code:
        to be displayed
    ~~~
    ~~~ {.output}
    output
    from
    program
    ~~~
    ~~~ {.error}
    error reports from program (if any)
    ~~~

    and possibly including:

    > ## Callout Box {.callout}
    >
    > An aside of some kind.

    > ## Key Points {.keypoints}
    >
    > * Key point 1
    > * Key point 2

    > ## Challenge Title {.challenge}
    >
    > Description of a single challenge.
    > There may be several challenges.

1. There are no sub-headings inside a topic other than the ones shown,
   and only one block of challenges at the end.
   If a topic needs sub-headings,
   it probably wants to be broken into two or more files.

2. Callout boxes are formatted as block quotes
   containing a level-2 heading having the `callout` class
   and some text, code, etc.

3. Each challenge is formatted in the same way,
   i.e., as a block quote with a level-2 heading having the `challenge` class.

Introductory Slides
-------------------

Every lesson must include a short slide deck suitable for a short presentation
(3 minutes or less)
that the instructor can use to explain to learners what the subject is,
how knowing it will help learners,
and what's going to be covered.
Slides are written in Markdown,
and compiled into HTML for use with [reveal.js](http://lab.hakim.se/reveal-js/).

    ---
    layout: slides
    ---
    body of slides

Glossary
--------

Each term in the glossary is laid out as a separate block quote,
with the term in a heading.
Yes, this is odd,
but as noted in the introduction,
we want to avoid putting HTML in Markdown,
and we can't add identifiers to paragraphs using `{#whatever}` notation:
that only works on headers.

    ---
    layout: glossary
    ---
    > ## First Term {#first-anchor}
    > The definition.
    > See also: [another word](#another-anchor)

    > ## Another Term {#another-anchor}
    > The definition.
    > See also: [first term](#some-anchor)

Reference Guide
---------------

The layout of the reference guide is up to the lesson's author.
The only thing required is the YAML header:

    ---
    layout: reference
    ---

Instructor's Guide
------------------

The instructor's guide is laid out as follows:

    ---
    layout: guide
    ---

    introductory text

    ## General Points

    1.  first point

    1.  second point (separated by blank line,
        may span multiple lines,
        starts with `1.` to indicate numbered list.

    ## Large Sub-Topic

    1.  first point on a sub-topic large enough to need a section

    1.  second point

Software and Data
-----------------

All of the software samples used in the lesson must go in a directory called `code/`.
Every sample must be listed in the file `code/index.md`,
which must be formatted as follows:

    ---
    layout: index
    ---
    * `filename.ext`: one-line description
    * `filename.ext`: one-line description

Stand-alone data files must go in a directory called `data/`.
Groups of related data files must be put together in a sub-directory of `data/`
with a meaningful (short) name.
Every data file or data set must be listed in the file `code/index.md`,
which must be formatted as follows:

    ---
    layout: index
    ---
    * `filename.ext`: one-line description
    * `sub-directory/`: one-line description

**Note:** This mirrors the layout a scientist would use for actual work
(see Noble's
"[A Quick Guide to Organizing Computational Biology Projects](http://www.ploscompbiol.org/article/info%3Adoi%2F10.1371%2Fjournal.pcbi.1000424)"
or Gentzkow and Shapiro's
"[Code and Data for the Social Sciences: A Practitioner's Guide](http://faculty.chicagobooth.edu/jesse.shapiro/research/CodeAndData.pdf)").
However,
it may cause novice learners problems.
If `code/program.py` includes a hard-wired path to a data file,
that path must be either `datafile.ext` or `data/datafile.ext`.
The first will only work if the program is run with the lesson's root directory as the current working directory,
while the second will only work if the program is run from within the `code/` directory.
This is a learning opportunity for students working from the command line,
but a confusing annoyance inside IDEs and the IPython Notebook
(where the tool's current working directory is less obvious).
And yes,
the right answer is to pass filenames on the command line,
but that requires learners to understand how to get command line arguments,
which isn't something they'll be ready for in the first hour or two.

Images
------

Images used in the lessons must go in an `img/` directory.
We strongly prefer SVG for line drawings,
since they are smaller, scale better, and are easier to edit.
Screenshots and other raster images must be PNG or JPEG format.
The `img/` directory does *not* need to have an `index.md` file.

Web Resources
-------------

Files used to generate the HTML version of a lesson are stored in the following directories:

* `web/css`: CSS style files
* `web/js`: Javascript files
* `web/img`: images such as logos and buttons
* `_layouts`: page layout templates
* `_includes`: inclusions in web pages, such as the standard header and footer

These files will usually not be edited by lesson authors.

Tools
-----

The `bin/` directory contains a program called `check.py`
that checks that the contents of the lesson conform to the rules above.

The lesson's root directory contains a `Makefile` with commands to manage lesson content.
Its targets are:

* `make`: without a target, this will print help.

* `make commands`: prints the same help.

* `make topic dd-slug`: create a new topic file with the given sequence number and slug.

* `make check`: run `bin/check.py` to make sure that everything is formatted properly,
  and print error messages identifying problems if it's not.

* `make site`: build the lesson website locally for previewing.
  This assumes `make check` has given the site a clean bill of health,
  and requires Pandoc.

* `make summary`: create a YAML-formatted summary of the lesson,
  including a list of the topics it includes,
  the terms it defines,
  the lesson's software requirements,
  etc.

* `make clean`: tidy up (i.e., delete the locally-built website).

**Note:** The Makefile should also include targets to turn IPython Notebooks into Markdown
and compare the result with the committed Markdown topic files,
and do equivalent conversions for other formats.

**Note:** The Makefile *should* contain targets to re-run code and check the output,
but there's no general way to do this
(and we're not about to build our own literate programming environment).
