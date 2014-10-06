---
layout: blog
root: ../../..
author: Gabriel A. Devenyi
title: "Of Templates and Metadata
date: 2014-10-06
time: "10:00:00"
category: ["Tooling"]
---
Greg recently posted as an appendix to the [splitting the repository post](http://software-carpentry.org/blog/2014/09/splitting-the-repo.html) a straw man template for how lessons might be structured after the repo split.
There a lot of good ideas there on how we can encourage good structure for lessons and help learners and instructors alike for software carpentry going forward.
This post is going to directly reference and comment on the content of that post so its considered mandatory reading to understand what I'm talking about.

# Templates and Metadata

First, I want to look at the templates from a slightly different perspective, how we should structure these templates in order to assist in programmatically building the site and the workshops, as well as assisting in sharing.
Some of these ideas have been discussed in a different context on Greg's post on [a new template for workshop websites](http://software-carpentry.org/blog/2014/10/a-new-template-for-workshop-websites.html).

To assist in the production of workshop websites and to better define the relationship between, lesson repositories should contain some metadata.
The YAML format seems to be a well-adopted and reasonably flexible format for storing metadata in files, in fact we're already using it as part of our existing Github-Jekyll workshop and site hosting.
The file ``index.md`` is the the sensible place to look for a lesson's metadata, as its the first thing people are writing and it should therefore be populated early in writing.

YAML headers on the top of the lessons would look like this:

```
---
title: "Beginner Shell"
authors: [Gabriel A. Devenyi, Greg Wilson]
---
```


Next is the question of what kind of metadata we might want to include.
The title of the lesson is essential since its not explicitly the name of any of the files.
The list of authors of the material could also live in a YAML header although there has also been discussion of extracting such information directly from the git history.
[There have recently been discussions](http://software-carpentry.org/blog/2014/09/sept-2014-lab-meeting-report.html) and an attempt to measure the amount of time required to teach lessons, including the (mean, median, average) time to present in the metadata allows someone constructing a multi-lesson workshop programmatically to determine if they have time to present all the material.
With the breakup of the lessons reposisotry into smaller chunks, and the proliferation of intermediate lessons, alternative lessons and extras, it would also be useful to specify "dependencies" for a given lesson.
The exact structure of how to define these dependencies is a little more tricky. If we structure all of lesson repositories the same, and we can convince other groups to also do this, we can specify dependencies as a github URL, either to a repository, or a repository and a specific commit.
This dependency system would allow two benefits:

1. warnings of the inclusion of lessons without their dependencies
2. optional automatic pull-in of lesson dependencies during construction of workshop sites

So here's what the YAML template might look like for a lesson:
```
title: "Beginner Shell"
authors: [Gabriel A. Devenyi, Greg Wilson]
present-time: "2h"
preq: [http://www.github.com/repo/commitid, http://www.github.com/anotherrepo]
```

The ``dd-slug.md`` files may also contain YAML metadata, perhaps similar bits such as the title and time estimate, or authors.
Having such data would allow further processing programmatically.

Tying this all together with the proposed ``make`` system discussed by Greg at [A New Template for Workshop Websites](http://software-carpentry.org/blog/2014/10/a-new-template-for-workshop-websites.html), we can construct a workshop that includes lessons from a number of lesson repositories, check dependencies, and construct a nice site.

# Content of new lesson repositories
Creating a new lesson that fits into the existing system needs to be quick and easy so that people are willing to share quickly.
There are several files which appear in the template list which should be optional:

- ``glossary.md``
- ``reference.md``

This content isn't core to lessons and I'm not even sure that anyone looks at it. I think we should examine the literature and Google analytics for our glossary to see if anyone is actually using it.
