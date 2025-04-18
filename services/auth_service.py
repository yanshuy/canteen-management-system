import sqlite3
import os

class AuthService:
    def __init__(self, db_path=None):
        # Use canteen.db in the database folder by default
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, 'database', 'canteen.db')
        self.db_path = db_path
        self._ensure_users_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _ensure_users_table(self):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def login(self, username, password):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT id, full_name, username, password FROM users WHERE username = ?', (username,))
            row = c.fetchone()
            if not row:
                return {"success": False, "message": "User not found"}
            db_id, full_name, db_username, db_password = row
            if db_password != password:
                return {"success": False, "message": "Invalid password"}
            return {
                "success": True,
                "user": {
                    "id": db_id,
                    "username": db_username,
                    "name": full_name
                }
            }

    def register(self, username, password, full_name):
        if not username or not password or not full_name:
            return {"success": False, "message": "All fields are required"}
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO users (full_name, username, password) VALUES (?, ?, ?)', (full_name, username, password))
                conn.commit()
            return {"success": True, "message": "User registered successfully"}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "Username already exists"}
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}