import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE comics(date INTEGER, transcript TEXT)''')

# Save the changes
conn.commit()

# Close the connection
conn.close()
