import time
import psycopg2
import os
import csv

# PostgreSQL connection details
DB_NAME = "TODO"      # TODO: Replace with your database name
DB_USER = "TODO"     # TODO: Replace with your username
DB_PASS = "TODO"   # TODO: Replace with your password
LOG_FILE = "/path/to/db_activity.log"  # TODO: Set the path for the log file
CSV_FILE = "/path/to/query_monitoring.csv"  # TODO: Set the path for the CSV output file

# Set environment variable to avoid password prompt
os.environ['PGPASSWORD'] = DB_PASS

# Get the total row count (N)
def get_total_row_count(cursor):
    cursor.execute("""
        SELECT n_live_tup AS row_count
        FROM pg_stat_user_tables
        WHERE relname = 'fruit';
    """)
    row = cursor.fetchone()
    return row[0] if row else 0

# Get the current idx_tup_read metric
def get_idx_tup_read(cursor):
    cursor.execute("""
        SELECT idx_tup_read
        FROM pg_stat_user_indexes
        WHERE relname = 'fruit';
    """)
    rows = cursor.fetchall()
    return sum(row[0] for row in rows) if rows else 0

# Monitor database activity and log it
def monitor_db():
    try:
        # Create connection and cursor
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
        conn.autocommit = True
        cursor = conn.cursor()

        # Get total row count (N) and initial idx_tup_read
        N = get_total_row_count(cursor)
        if N == 0:
            print("Unable to get total row count, exiting.")
            return
        
        initial_idx_tup_read = get_idx_tup_read(cursor)

        # Open log and CSV files
        with open(LOG_FILE, "a") as log_file, open(CSV_FILE, "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['User', 'SQL Query', 'Rows Affected', 'Percentage Change'])

            # Monitor queries until the first one is detected
            while True:
                cursor.execute("""
                    SELECT pid, usename, query, state
                    FROM pg_stat_activity
                    WHERE state = 'active' AND usename <> 'postgres';
                """)

                rows = cursor.fetchall()

                if rows:
                    # Process only the first query
                    pid, usename, query, state = rows[0]

                    if pid and usename and query and state:
                        log_file.write(f"{pid}, {usename}, {query}, {state}\n")
                        log_file.flush()
                        
                        # Wait for metrics to stabilize
                        time.sleep(2)
                        
                        # Calculate the impact of the query
                        current_idx_tup_read = get_idx_tup_read(cursor)
                        idx_diff = current_idx_tup_read - initial_idx_tup_read
                        print(f"Initial idx_tup_read: {initial_idx_tup_read}, Current idx_tup_read: {current_idx_tup_read}, Difference: {idx_diff}")

                        # Calculate and log results if query activity is detected
                        if idx_diff > 0:
                            percentage_change = (idx_diff / N) * 100 if N > 0 else 0
                            rows_affected = idx_diff
                            csv_writer.writerow([usename, query, rows_affected, percentage_change])

                            # Update initial idx_tup_read for next calculation
                            initial_idx_tup_read = current_idx_tup_read

                    # Stop monitoring after one query
                    break

                time.sleep(0.00001)

    except KeyboardInterrupt:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Start monitoring
if __name__ == "__main__":
    monitor_db()
