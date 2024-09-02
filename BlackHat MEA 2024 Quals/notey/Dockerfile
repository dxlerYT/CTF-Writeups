FROM node:14 AS final

# Install dependencies
RUN apt-get update && apt-get install -y socat mariadb-server libpng-dev

# Set the working directory in the container
WORKDIR /app

# Install Node.js dependencies
RUN npm install express express-session mysql path mariadb

COPY init.db /

# Run mysql temporarily to create the database
ENV USER="ctf"
ENV PASSWORD="redacted"
RUN /etc/init.d/mysql start && \
    mysql -uroot -e "CREATE USER '${USER}'@'localhost' IDENTIFIED BY '${PASSWORD}';" && \
    mysql -uroot -e "GRANT SELECT, INSERT, UPDATE, CREATE, DROP ON *.* TO '${USER}'@'localhost';" && \
    mysql -uroot -e "FLUSH PRIVILEGES;" && \
    mysql -u$USER -p$PASSWORD -e "CREATE database CTF;" && \
    mysql -u$USER -p$PASSWORD CTF < /init.db && \
    /etc/init.d/mysql stop && \
    chmod -R 777 /var/lib/mysql /var/run/mysqld /var/log/mysql && \
    rm /init.db

# Copy the entire application code to the working directory
COPY src/ .

FROM pwn.red/jail
COPY --from=final / /srv
COPY docker-entrypoint.sh /srv/app/run
COPY hook.sh /jail/hook.sh
RUN chmod +x /srv/app/run /jail/hook.sh && \
    touch /srv/flag.txt && chmod 777 /srv/flag.txt && \
    echo "127.0.0.1 debuerreotype localhost app" >> /srv/etc/hosts
ENV JAIL_PIDS=0 JAIL_CPU=0 JAIL_MEM=0 JAIL_TIME=0 JAIL_TMP_SIZE=100M JAIL_DEV=null,zero,urandom
