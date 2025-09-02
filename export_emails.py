import os
import psycopg2
import csv

TABLE_NAME = "email"  # change this to the table you want
CSV_FILE = "emails.csv"

# Use localhost and default port 5432 because we'll use fly postgres connect tunnel
DB_HOST = "localhost"
DB_PORT = 5432

# Try to get credentials from environment variables
DB_NAME = os.environ.get("FLY_DB_NAME") or input("Enter database name: ")
DB_USER = os.environ.get("FLY_DB_USER") or input("Enter database user: ")
DB_PASSWORD = os.environ.get("FLY_DB_PASSWORD") or input("Enter database password: ")

# Connect to Postgres via the tunnel
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    sslmode="require",
)

cur = conn.cursor()

# Export table to CSV
with open(CSV_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)

    # Write header
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """,
        (TABLE_NAME,),
    )
    headers = [row[0] for row in cur.fetchall()]
    writer.writerow(headers)

    # Write data
    cur.execute(f"SELECT * FROM {TABLE_NAME};")
    for row in cur.fetchall():
        writer.writerow(row)

print(f"✅ Exported table '{TABLE_NAME}' to '{CSV_FILE}'")

cur.close()
conn.close()
