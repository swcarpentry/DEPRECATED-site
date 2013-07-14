SRC_ROOT = $(wildcard ./*.html)
SRC_BLOG = $(wildcard ./blog/????/??/*.html)
SRC_BOOTCAMP = $(wildcard ./bootcamps/????-??-*/index.html)
SRC_BADGES = ./badges/index.html
SRC_V3 = $(wildcard ./v3/*.html)
SRC_V4 = ./v4/index.html $(wildcard ./v4/*/*.html)
SRC_LAYOUT = $(wildcard ./_layouts/*.html)
SRC_INCLUDES = $(wildcard ./_includes/*.html) $(wildcard ./_includes/*/*.html)
SRC_PAGES = \
    $(SRC_ROOT) \
    $(SRC_ABOUT) \
    ./blog/index.html $(SRC_BLOG) \
    ./bootcamps/index.html $(SRC_BOOTCAMPS) \
    $(SRC_BADGES) \
    $(SRC_V3) \
    $(SRC_V4) \
    $(SRC_LAYOUT) \
    $(SRC_INCLUDES)

GENERATED = ./_config.yml ./_includes/recent_blog_posts.html

DST_DIRS = $(OUT)/css $(OUT)/img $(OUT)/js

#----------------------------------------

all : commands

## commands : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

## check    : build locally into _site directory for checking
check :
	@make SITE=$(PWD)/_site OUT=$(PWD)/_site build

## clean    : clean up
clean :
	rm -rf $(GENERATED) _site $$(find . -name '*~' -print)

#----------------------------------------

# build : compile site into $(OUT) with $(SITE) as Software Carpentry base URL
build : $(OUT)/bootcamps.ics $(OUT)/feed.xml $(OUT)/.htaccess $(DST_DIRS)

$(OUT)/.htaccess : ./_htaccess
	cp $< $@

$(OUT)/css : ./css
	cp -r $< $@

$(OUT)/img : ./img
	cp -r $< $@

$(OUT)/js : ./js
	cp -r $< $@

$(OUT)/bootcamps.ics : ./bin/calendar.py $(OUT)/index.html
	python ./bin/calendar.py -o $(OUT) -s $(SITE)

$(OUT)/feed.xml : ./bin/feed.py $(OUT)/index.html
	python ./bin/feed.py -o $(OUT) -s $(SITE)

$(SITE)/index.html : _config.yml $(SRC_PAGES)
	jekyll $(OUT)

_config.yml : ./bin/preprocess.py standard_config.yml $(SRC_BLOG) $(SRC_BOOTCAMP)
	python ./bin/preprocess.py -o $(OUT) -s $(SITE)
