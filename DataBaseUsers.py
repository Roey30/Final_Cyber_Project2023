import sqlite3

username_password_storage = sqlite3.connect("username_password_storage.db")

user = username_password_storage.cursor()

user.execute("""CREATE TABLE IF NOT EXISTS username_password_storage (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             password TEXT,
             permission INTEGER
             )""")

username_password_storage.commit()
username_password_storage.close()
