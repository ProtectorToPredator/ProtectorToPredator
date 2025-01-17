import time
import psycopg2
import os

# PostgreSQL Connection Information
DB_NAME = "TODO"      # Replace with your database name
DB_USER = "TODO"      # Replace with your username
DB_PASS = "TODO"      # Replace with your password
LOG_FILE = "TODO"     # Path to the log file (Replace with your desired path)

# Set environment variable to avoid password prompt every time
os.environ['PGPASSWORD'] = DB_PASS

# Function to monitor database activity and log queries
def monitor_db():
    try:
        # Establish database connection (connect only once)
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
        conn.autocommit = True
        print("Database connection established successfully!")
        cursor = conn.cursor()

        # Open the log file and keep the file stream open for appending
        with open(LOG_FILE, "a") as log_file:
            while True:
                # Execute query to monitor active database connections
                cursor.execute("""
                    SELECT pid, usename, query, state
                    FROM pg_stat_activity
                    WHERE state = 'active' AND usename <> 'postgres';
                """)

                rows = cursor.fetchall()

                # If there are active queries, write them to the log file
                if rows:
                    for row in rows:
                        pid, usename, query, state = row
                        if pid and usename and query and state:
                            log_file.write(f"{pid}, {usename}, {query}, {state}\n")
                    log_file.flush()  # Ensure immediate writing to the file

                # Wait for a very short time (0.00001 seconds)
                time.sleep(0.00001)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Start the monitoring process
if __name__ == "__main__":
    monitor_db()
