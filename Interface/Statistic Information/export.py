# -*- coding: utf-8 -*-

import psycopg2
import csv

# Database connection configuration
db_config = {
    'host': 'TODO',        # Replace with your database host
    'port': 'TODO',        # Replace with your database port if different
    'database': 'TODO',    # Replace with your database name
    'user': 'TODO',        # Replace with your database username
    'password': 'TODO'     # Replace with your database password
}

# SQL query to retrieve statistics for the 'fruit' table
query = """
SELECT *                    
FROM pg_statistic
WHERE starelid = (SELECT oid FROM pg_class WHERE relname = 'fruit' 
                  AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public'));
"""

# Output CSV file path
output_csv_file = "TODO"  # Replace with your desired file path for output CSV

try:
    # Establish connection to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Extract column names

    # Write the results to a CSV file
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write column headers
        writer.writerows(rows)    # Write data rows

    print("Query results successfully exported to {}".format(output_csv_file))

except Exception as e:
    print("An error occurred: {}".format(e))

finally:
    # Ensure the cursor and connection are closed
    if cursor:
        cursor.close()
    if conn:
        conn.close()
