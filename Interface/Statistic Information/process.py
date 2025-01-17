# -*- coding: utf-8 -*-

import pandas as pd
import psycopg2

# Path to the CSV file (TODO: Replace with actual path)
csv_file = "TODO"  # Path to the CSV file

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Database connection configuration (TODO: Replace with actual credentials)
db_config = {
    'host': 'TODO',        # Replace with your database host
    'port': 'TODO',        # Database port
    'database': 'TODO',    # Replace with your database name
    'user': 'TODO',        # Replace with your username
    'password': 'TODO'     # Replace with your password
}

# Function to get the total row count from the database
def get_total_row_count():
    query = """
    SELECT n_live_tup AS row_count
    FROM pg_stat_user_tables
    WHERE relname = 'fruit';
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"An error occurred while fetching row count: {e}")
        return 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to transform stadistinct into a meaningful unique value rate
def calculate_unique_rate_percentage(stadistinct):
    if stadistinct < 0:
        return f"Estimated: {-stadistinct * 100:.2f}% of total rows"
    else:
        return f"Exact: {stadistinct} unique values"

# Function to transform stadistinct into a unique count
def calculate_unique_count(stadistinct, total_rows):
    if stadistinct < 0:
        return -stadistinct * total_rows
    else:
        return stadistinct

# Function to process the DataFrame and generate structured output
def process_statistic_data(df, total_rows):
    output = ""
    for index, row in df.iterrows():
        output += f"attr{row['staattnum']}:\n"
        output += f"    ——stanullfrac={row['stanullfrac']}\n"
        unique_rate = calculate_unique_rate_percentage(row['stadistinct'])
        unique_count = calculate_unique_count(row['stadistinct'], total_rows)
        output += f"    —— Unique value rate: {unique_rate}\n"
        output += f"    —— Unique value count: {unique_count}\n"

        if row['stakind1'] == 1:
            output += "    —— stakind1=1\n"
            output += f"        —— Most common values: {row['stavalues1']}\n"
            output += f"        —— Frequencies: {row['stanumbers1']}\n"

        if row['stakind1'] == 2 or row['stakind2'] == 2:
            output += "    —— stakind=2\n"
            output += f"        —— Histogram bounds: {row['stavalues1']}\n"

    return output

# Get the total row count from the database
total_rows = get_total_row_count()
print(f"Total rows in 'fruit': {total_rows}")

# Generate the structured output
structured_output = process_statistic_data(df, total_rows)

# Save the structured output to a text file (TODO: Replace with actual path)
output_file = "TODO"  # Path to save the output text file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(structured_output)

print(f"Processed data has been saved to {output_file}")
