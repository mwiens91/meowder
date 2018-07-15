# Dockerfile for meowder Travis build

# Use Ubuntu base image
FROM ubuntu:18.04

# Environment vars
ENV TZ=Canada/Vancouver \
    DEBIAN_FRONTEND=noninteractive

# Get the packages we need
RUN apt update
RUN apt install -y git \
                   python3-dev python3-pip \
                   libpq-dev postgresql postgresql-contrib

# Clone meowder
RUN git clone https://github.com/mwiens91/meowder.git /meowder

# Install requirements
RUN pip3 install -r /meowder/requirements.txt

# Set up .env file
RUN cp /meowder/.env.example /meowder/.env

# Run the rest of the commands as the "postgres" user to set up the
# meowder database
USER postgres

RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE DATABASE meowder;" &&\
    psql --command "CREATE USER johnsmith WITH PASSWORD 'johnsmithspassword';" &&\
    psql --command "ALTER ROLE johnsmith SET client_encoding TO 'utf8';" &&\
    psql --command "ALTER ROLE johnsmith SET default_transaction_isolation TO 'read committed';" &&\
    psql --command "ALTER ROLE johnsmith SET timezone TO 'UTC';" &&\
    psql --command "GRANT ALL PRIVILEGES ON DATABASE meowder TO johnsmith;"

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/10/bin/postgres", "-D", "/var/lib/postgresql/10/main", "-c", "config_file=/etc/postgresql/10/main/postgresql.conf"]
