for i in caporaso.greg clayton.sophie gross.jonathan oleary.aaron pritchard.leighton soontiens.nancy srinath.ashwin tatman.rachael timbers.tiffany white.samuel
do
    python bin/badge-create.py $(sqlite3 ~/s/admin/roster.db 'select person || " " || email || " instructor" from person where person="'$i'";')
done
