import sqlite3

# Connect to the database
conn = sqlite3.connect('picture_database.db')

# Create the pictures table
conn.execute('''CREATE TABLE PICTURES
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             NAME TEXT,
             FILE_PATH TEXT,
             Version INTEGER);''')

# Insert a picture into the table
conn.execute("INSERT INTO PICTURES (ID, NAME, FILE_PATH) \
                  VALUES (1, 'Picture 1', '/path/to/picture1.jpg')")

# Query the database for pictures
cursor = conn.execute("SELECT * FROM PICTURES")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("FILE_PATH = ", row[2])
    print("Version = ", row[3])

# Close the connection
conn.close()
