(for i in $(cat foo); do echo python bin/badge-create.py $i $(sqlite3 ~/s/admin/roster.db "select email from person where person='$i';") instructor; done) | bash
