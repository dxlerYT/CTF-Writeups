#!/bin/sh
service mysql restart
USER="ctf"
PASSWORD="ctf123"

echo "Creating new user ${USER} ..."
mysql -uroot -e "CREATE USER '${USER}'@'localhost' IDENTIFIED BY '${PASSWORD}';"
echo "Granting privileges..."
mysql -uroot -e "GRANT SELECT, INSERT, UPDATE, CREATE, DROP ON *.* TO '${USER}'@'localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"
echo "Done! Permissions granted"
mysql -u$USER -p$PASSWORD -e "CREATE database CTF;"
mysql -u$USER -p$PASSWORD CTF  < /init.db
echo "All done."

node /app/index.js&
service mysql start && tail -f /dev/null
