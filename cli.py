import sys
from authentication import Authentication
from database import Database

def print_instructions():
    print("Welcome to the Authentication System CLI!")
    print("Choose an option:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

def after_login_instructions():
    print("\nWhat would you like to do next?")
    print("1. Validate Token")
    print("2. Exit")

def register_user(auth):
    print("\n--- Register ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    success, message = auth.register(username, password, email, phone)
    print(message)

def login_user(auth):
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    success, message, token = auth.login(username, password)
    if success:
        print(f"{message} Your token is: {token}")
        after_login_options(auth, token)
    else:
        print(message)

def after_login_options(auth, token):
    after_login_instructions()
    choice = input("Enter your choice (1/2): ")
    if choice == '1':
        validate_token(auth, token)
    elif choice == '2':
        print("Exiting...")
        sys.exit()

def validate_token(auth, token):
    valid, username_or_message = auth.verify_token(token)
    if valid:
        print(f"Token is valid for user: {username_or_message}")
    else:
        print(username_or_message)

def main():
    db = Database()
    auth = Authentication(db)

    while True:
        print_instructions()
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            register_user(auth)
        elif choice == '2':
            login_user(auth)
        elif choice == '3':
            print("Exiting...")
            db.close()
            sys.exit()
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
