
from validator import Validator
from password_hasher import PasswordHasher
from user_repository import UserRepository
from audit_logger import AuditLogger
from auth_service import AuthService


validator = Validator()
password_hasher = PasswordHasher()
repository = UserRepository()
audit_logger = AuditLogger()

auth_service = AuthService(
    validator,
    password_hasher,
    repository,
    audit_logger
)

auth_service.create_default_admin()


while True:
    print("\n===== STUDENT PORTAL =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if choice == 1:
        print("--- Student Registration ---")
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        auth_service.register(username, email, password)

    elif choice == 2:
        print("--- Login ---")
        username = input("Username: ")
        password = input("Password: ")

        auth_service.login(username, password)

        if auth_service.current_user is not None:
            auth_service.current_user.show_dashboard()

            while auth_service.current_user is not None:
                print("===== USER MENU =====")
                print("1. View available options")
                print("2. Change Password")
                print("3. Logout")

                try:
                    user_choice = int(input("Enter your choice: "))
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                if user_choice == 1:
                    auth_service.show_menu()

                elif user_choice == 2:
                    old_password = input("Current Password: ")
                    new_password = input("New Password: ")

                    auth_service.change_password(
                        old_password, new_password
                    )

                elif user_choice == 3:
                    auth_service.logout()

                else:
                    print("Invalid option.")

    elif choice == 3:
        print("Thank you for using Student Portal!")
        break

    else:
        print("Invalid option.")
