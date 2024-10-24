import sqlite3 as sq

conn = sq.connect('devices.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()
conn.close()
print("Database setup complete.")
