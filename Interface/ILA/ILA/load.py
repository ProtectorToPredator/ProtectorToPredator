import pandas as pd
import psycopg2
from io import StringIO

# Database connection parameters
hostname = 'TODO: Enter hostname'  # e.g., '127.0.0.1'
username = 'TODO: Enter username'  # e.g., 'postgres'
password = 'TODO: Enter password'  # e.g., 'your_password'
database = 'TODO: Enter database name'  # e.g., 'disease'

# Path to the CSV file (adjust for your system)
csv_file_path = '/home/user/mydataset/diabetes_012_health_indicators_BRFSS2015.csv'  # TODO: Set the correct path

# Read CSV file, skipping the first row
data = pd.read_csv(csv_file_path, skiprows=1)

# Convert all columns to integer type
data = data.astype(int)

# Establish connection to the PostgreSQL database
conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
cursor = conn.cursor()

# Execute specific SQL statements to enable debug mode (optional)
cursor.execute("SELECT enable_debug_mode(1);")  # Ensure that the function exists in your DB

# Convert the DataFrame to an in-memory CSV format for the COPY command
output = StringIO()
data.to_csv(output, sep='\t', header=False, index=False)  # Use tab separator
output.seek(0)  # Rewind the StringIO object to the beginning

# Use the COPY command to import data into the PostgreSQL table
table_name = 'disease1'  # TODO: Replace with the actual table name
cursor.copy_from(output, table_name, null="")  # Ensure that the table columns match the data
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data imported successfully.")
