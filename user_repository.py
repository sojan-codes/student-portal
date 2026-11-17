import json
import os
from user import Student, Teacher, Admin


class UserRepository:
    def __init__(self):
        self.users = {}
        self.file_path = "users.json"
        self.load_users()

    def save_users(self):
        user_data = {}
        for key, value in self.users.items():
            user_data[key] = {
                "username": value.username,
                "email": value.email,
                "role": value.role,
                "password_hash": value.password_hash,
                "salt": value.salt,
                "failed_login_attempts": value.failed_login_attempts,
                "is_locked": value.is_locked,
            }
        with open(self.file_path, "w") as file:
            json.dump(user_data, file, indent=4)

    def username_exists(self, username):
        return username in self.users

    def add_user(self, user):
        self.users[user.username] = user
        self.save_users()

    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        return None

    def load_users(self):
        if os.path.exists(self.file_path):
            with open("users.json", "r") as data:
                user_data = json.load(data)
                for username, details in user_data.items():
                    if details["role"] == "Student":
                        user = Student(
                            details["username"],
                            details["email"],
                            details["role"],
                            details["password_hash"],
                            details["salt"],
                        )
                        self.users[username] = user
                    elif details["role"] == "Teacher":
                        user = Teacher(
                            details["username"],
                            details["email"],
                            details["role"],
                            details["password_hash"],
                            details["salt"],
                        )
                        self.users[username] = user
                    elif details["role"] == "Admin":
                        user = Admin(
                            details["username"],
                            details["email"],
                            details["role"],
                            details["password_hash"],
                            details["salt"],
                        )
                        self.users[username] = user
                    user.restore_account_status(
                        details["failed_login_attempts"], 
                        details["is_locked"]
                    )
