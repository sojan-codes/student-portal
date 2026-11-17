from user import Student, Teacher, Admin
from decorators import requires_permission


class AuthService:
    def __init__(self, validator, password_hasher, repository, audit_logger):
        self.validator = validator
        self.password_hasher = password_hasher
        self.repository = repository
        self.audit_logger = audit_logger
        self.current_user = None

    def register(self, username, email, password):
        username_errors = self.validator.validate_username(username)
        email_errors = self.validator.validate_email(email)
        password_errors = self.validator.validate_password(password)

        errors = username_errors + email_errors + password_errors
        if not errors:
            print("Validation successful")
        else:
            for error in errors:
                print(error)
            return

        if self.repository.username_exists(username):
            print("Username already exists.")
            return

        salt = self.password_hasher.generate_salt()
        password_hash = self.password_hasher.hash_password(password, salt)

        student = Student(username, email, "Student", password_hash, salt)

        self.repository.add_user(student)
        print("Registration successful!")

        self.audit_logger.log_event(username, "Registration Successful")

    def login(self, username, password):
        user = self.repository.get_user(username)

        if user is None:
            print("User Not Found.")
            return

        if user.is_locked:
            print("Account is Locked")
            return

        is_valid = self.password_hasher.verify_password(
            password, user.salt, user.password_hash
        )
        if is_valid:
            print("Login Successful")
            user.reset_failed_attempts()
            self.repository.save_users()
            self.audit_logger.log_event(username, "Login Successful")
            self.current_user = user
            # user.reset_failed_attempts()
        else:
            user.record_failed_attempt()
            self.repository.save_users()
            print("Incorrect Password")
            self.audit_logger.log_event(username, "Login Failed")

    def logout(self):
        if self.current_user is None:
            print("No user is currently logged in.")
        else:
            self.audit_logger.log_event(self.current_user.username, "Logout Successful")
            self.current_user = None
            print("Logout successful!")

    def change_password(self, old_password, new_password):
        if self.current_user is None:
            return
        if not self.password_hasher.verify_password(
            old_password, self.current_user.salt, self.current_user.password_hash
        ):
            print("Wrong Password.")
            return
        if self.validator.validate_password(new_password):
            for error in self.validator.validate_password(new_password):
                print(error)
            return
        new_salt = self.password_hasher.generate_salt()
        new_hash = self.password_hasher.hash_password(new_password, new_salt)
        self.current_user.update_password(new_hash, new_salt)
        print("Password updated successfully!")
        self.repository.save_users()
        self.audit_logger.log_event(self.current_user.username, "Password Changed")

    def has_permission(self, permission):
        if self.current_user is None:
            return False
        if permission in self.current_user.get_permissions():
            return True
        return False

    def show_menu(self):
        if self.current_user is None:
            return
        menu = {
            "view_profile": "View Profile",
            "view_courses": "View Courses",
            "view_grades": "View Grades",
            "manage_grades": "Manage Grades",
            "view_students": "View Students",
            "manage_users": "Manage Users",
            "manage_roles": "Manage Roles",
            "view_audit_logs": "View Audit Logs",
        }
        # if self.current_user.role.lower() == "admin":
        #     for role in self.current_user.get_permissions():
        #         print(menu[role])
        # elif self.current_user.role.lower() == "teacher":
        #     for role in self.current_user.get_permissions():
        #         print(menu[role])
        # elif self.current_user.role.lower() == "student":
        #     for role in self.current_user.get_permissions():
        #         print(menu[role])
        count = 1
        user_permissions = []
        for permission in sorted(self.current_user.get_permissions()):
            print(count, menu[permission])
            user_permissions.append(permission)
            count += 1
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            return
        if choice > 0 and choice <= len(user_permissions):
            selected_permission = user_permissions[choice - 1]
            if selected_permission == "view_profile":
                print(self.current_user)
            elif selected_permission == "view_courses":
                print("Displaying Available Courses...")
            elif selected_permission == "view_grades":
                print("Displaying Student Grades...")
            elif selected_permission == "manage_grades":
                print("Managing Student Grades...")
            elif selected_permission == "view_students":
                print("Viewing Students...")
            elif selected_permission == "manage_users":
                username = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                role = input("Enter role (Teacher/Admin): ")

                self.create_user(username, email, password, role)
            elif selected_permission == "manage_roles":
                print("Managing Roles...")
            elif selected_permission == "view_audit_logs":
                self.view_audit_logs()
        else:
            print("Invalid Option")

    @requires_permission("view_audit_logs")
    def view_audit_logs(self):
        logs = self.audit_logger.get_recent_logs()

        for log in logs:
            print(log, end="")

    @requires_permission("manage_users")
    def create_user(self, username, email, password, role):
        role = role.capitalize()
        if self.repository.get_user(username) is not None:
            print("User Exists.")
            return
        username_errors = self.validator.validate_username(username)
        password_errors = self.validator.validate_password(password)
        email_errors = self.validator.validate_email(email)

        if username_errors:
            for error in username_errors:
                print(error)
            return

        if password_errors:
            for error in password_errors:
                print(error)
            return

        if email_errors:
            for error in email_errors:
                print(error)
            return

        if role.lower() not in ("teacher", "admin"):
            print("Invalid role")
            return
        salt = self.password_hasher.generate_salt()

        password_hash = self.password_hasher.hash_password(password, salt)
        if role.lower() == "teacher":
            user = Teacher(username, email, role, password_hash, salt)
            self.repository.add_user(user)
            print("Teacher account created successfully!")
            self.audit_logger.log_event(username, f"{role} Account Created")
        elif role.lower() == "admin":
            user = Admin(username, email, role, password_hash, salt)
            self.repository.add_user(user)
            print("Admin account created successfully!")
            self.audit_logger.log_event(username, f"{role} Account Created")

    def create_default_admin(self):
        if self.repository.users:
            return

        username = "admin"
        email = "admin@example.com"
        password = "Admin@123"

        salt = self.password_hasher.generate_salt()
        password_hash = self.password_hasher.hash_password(password, salt)

        admin = Admin(username, email, "Admin", password_hash, salt)

        self.repository.add_user(admin)

        print("Default Admin account created!")
        print("Username:", username)
        print("Password:", password)


# from user import Student
# student = Student(
#     "ram123",
#     "ram@gmail.com",
#     "Student",
#     "sample_hash",
#     "sample_salt"
# )
# print(student.username)
# print(student.get_permissions())
