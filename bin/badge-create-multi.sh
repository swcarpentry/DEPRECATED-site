#!/usr/bin/env bash
# Usage: badge-create-multi.sh user.name user.name
for i in $*
do
    python bin/badge-create.py $(sqlite3 ~/s/admin/roster.db 'select person || " " || email || " instructor" from person where person="'$i'";')
done
