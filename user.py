from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, username, email, role, password_hash, salt):
        self.__username = username
        self.__email = email
        self.__role = role
        self.__password_hash = password_hash
        self.__salt = salt
        self.__failed_login_attempts = 0
        self.__is_locked = False

    def record_failed_attempt(self):
        self.__failed_login_attempts += 1
        if self.__failed_login_attempts == 3:
            self.__is_locked = True
            print("Account locked after 3 failed login attempts.")

    def reset_failed_attempts(self):
        self.__failed_login_attempts = 0

    @property
    def is_locked(self):
        return self.__is_locked

    @property
    def failed_login_attempts(self):
        return self.__failed_login_attempts

    @abstractmethod
    def show_dashboard(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def role(self):
        return self.__role

    @property
    def password_hash(self):
        return self.__password_hash

    @property
    def salt(self):
        return self.__salt

    def update_password(self, new_hash, new_salt):
        self.__password_hash = new_hash
        self.__salt = new_salt

    def __str__(self):
        return f"Username: {self.username} \nEmail: {self.email} \nRole: {self.role}"

    def restore_account_status(self, failed_attempts, is_locked):
        self.__failed_login_attempts = failed_attempts
        self.__is_locked = is_locked


class Student(User):
    def show_dashboard(self):
        print("Welcome to Student Dashboard")

    def get_permissions(self):
        permissions = {"view_profile", "view_courses", "view_grades"}
        return permissions


class Teacher(User):
    def show_dashboard(self):
        print("Welcome to Teacher Dashboard")

    def get_permissions(self):
        permissions = {"view_profile", "view_courses", "manage_grades", "view_students"}
        return permissions


class Admin(User):
    def show_dashboard(self):
        print("Welcome to Admin Dashboard")

    def get_permissions(self):
        permissions = {
            "view_profile",
            "view_courses",
            "manage_users",
            "manage_roles",
            "view_audit_logs",
            "manage_grades",
        }
        return permissions


# users = [
#     Student("ram", "ram@gmail.com", "Student"),
#     Teacher("hari", "hari@gmail.com", "Teacher"),
#     Admin("admin", "admin@gmail.com", "Admin")
# ]

# for user in users:
#     user.show_dashboard()
