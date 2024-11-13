#!/bin/bash

export PGUSER="$POSTGRES_USER"

psql -c "CREATE DATABASE $POSTGRES_DB"

psql -d $POSTGRES_DB -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

echo "Database $POSTGRES_DB and user $POSTGRES_USER initialized successfully."