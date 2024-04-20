import sqlite3

class Database:
    def __init__(self, db_name='authentication.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password TEXT,
                            email TEXT,
                            phone TEXT
                        )''')
        self.conn.commit()

    def register_user(self, username, password, email, phone):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
                           (username, password, email, phone))
            self.conn.commit()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def get_user_info(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_info = cursor.fetchone()
        return user_info


    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    db.close()
