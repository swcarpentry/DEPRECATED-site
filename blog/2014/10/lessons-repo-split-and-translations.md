---
layout: blog
root: ../../..
author: Gabriel A. Devenyi
title: "Lessons, the repository split, and translations"
date: 2014-10-06
time: "14:00:00"
category: ["Tooling"]
---
Keeping on the roll of the posts about the [repo split](), [templates](), and [metadata](), Software Carpentry's trajectory appears to reaching the point of needing to consider how to handle translated lessons.
The purpose of this post is examine the various options of how we might handle translations, rather than propose a specific solution to the translation problem.

## Option 1: Translations live within the lesson repo

The first (and most straightforward?) method of handling translations is to introduce a ``translations`` directory to the existing lesson templates.
Under this directory would live translations other than original lesson using the ISO two-letter language code.
The contents of these directories would be otherwise identical to those of the host lesson.

## Option 2: Translations live within a separate branch

Branches could be created of the form ``trans-ISOCODE`` from the existing lessons.
This would improve the ability to track the master language of the lesson and rebase changes (which would then need to be translated) as the lesson is updated.

## Option 3: Translations live within a forked repo

Repositories containing translations could be forked from the main lesson and be maintained separately from the original.
Changes would have to be merged from upstream and then translated.

## How official is a translation?

Integrating the translations into the lesson repository, either as Option 1 or Option 2, lends a certain endorsement of the quality and completeness of the translation. This may impose a burden on the lesson maintainers to either translate themselves (in the case where they have the ability) or attempt to seek out translators to maintain existing material. Barring that, they will have to decide when the core lesson has diverged too much from a translation, and "depreciate" the material. 
