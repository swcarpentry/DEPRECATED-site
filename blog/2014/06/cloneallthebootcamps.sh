#!/bin/bash

# This script scrapes the software carpentry webiste for the urls of upcoming bootcamps,
# tries to clone all of them, and tests them for the presecnce of the 'aux' directory
# which breaks cloning on Windows.                              
# See https://github.com/swcarpentry/bc/issues/463
# 2014-06-12 

# Download the webpage containing links to upcoming bootcamp github.io websites
curl  http://software-carpentry.org/bootcamps/index.html  > upcomingworkshops.html

# extract URLS poiting to github.io 
cat upcomingworkshops.html | grep http | sed 's/.*http:/http:/; s/\/".*//;' | grep github.io  > upcoming-webpages.txt

# convert URLS of the form http://instructor.github.io/reponame to http://github.com/instructor/reponame using sed
cat upcoming-webpages.txt | tr '\.' ' '  | tr '/' ' ' | awk '{print "http://github.com/" $2 "/" $5 }'  > upcoming-github.txt

# clone all the things   Note: does not capture output of git clone.
cat upcoming-github.txt | xargs -n 1  git clone

# check (on linux or osx) for the file that Windows cannot bear
# echo These repositories need to be fixed:
find 2014* -name aux

