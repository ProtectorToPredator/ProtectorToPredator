#!/bin/bash

# PostgreSQL Connection Information
DB_NAME="TODO"     # Replace with your database name
DB_USER="TODO"    # Replace with your username
DB_PASS="TODO"  # Replace with your password
LOG_FILE="TODO"  # Path to the log file (Replace with your desired path)

# Set environment variable to avoid password prompt every time
export PGPASSWORD="$DB_PASS"

# Infinite loop to continuously execute the query
while true; do
    # Use psql to execute the query and filter out records where the username is not 'postgres'
    psql -U "$DB_USER" -d "$DB_NAME" -t -c "
        SELECT pid, usename, query, state
        FROM pg_stat_activity
        WHERE state = 'active' AND usename <> 'postgres';
    " | while read -r pid usename query state; do
        # If data is returned, write each line to the log file
        if [[ -n "$pid" && -n "$usename" && -n "$query" && -n "$state" ]]; then
            echo "$pid, $usename, $query, $state" >> "$LOG_FILE"
        fi
    done

    # Wait for 0.00001 seconds (10 microseconds)
    sleep 0.00001
done
