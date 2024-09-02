#!/bin/bash
/usr/bin/mysqld_safe --skip-syslog --skip-kill-mysqld --socket=/var/run/mysqld/mysqld.sock --pid-file=/var/run/mysqld/mysqld.pid --user=mysql --datadir=/var/lib/mysql --log-error=/tmp/mysql_error.log >/dev/null 2>&1 &
#node /app/index.js
(&>/dev/null node /app/index.js)&
socat - TCP:127.0.0.1:3000,forever
