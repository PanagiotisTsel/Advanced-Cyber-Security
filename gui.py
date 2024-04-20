import tkinter as tk
from tkinter import messagebox
from authentication import Authentication
from database import Database

class AuthApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Authentication System")
        self.db = Database()
        self.auth = Authentication(self.db)

        # Main Frame
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Buttons
        tk.Button(self.frame, text="Register", command=self.register).grid(row=0, column=0)
        tk.Button(self.frame, text="Login", command=self.login).grid(row=1, column=0)
        tk.Button(self.frame, text="Exit", command=self.exit_app).grid(row=2, column=0)

    def register(self):
        self.clear_frame()
        tk.Label(self.frame, text="Username:").grid(row=0, column=0)
        username = tk.Entry(self.frame)
        username.grid(row=0, column=1)
        tk.Label(self.frame, text="Password:").grid(row=1, column=0)
        password = tk.Entry(self.frame, show="*")
        password.grid(row=1, column=1)
        tk.Label(self.frame, text="Email:").grid(row=2, column=0)
        email = tk.Entry(self.frame)
        email.grid(row=2, column=1)
        tk.Label(self.frame, text="Phone:").grid(row=3, column=0)
        phone = tk.Entry(self.frame)
        phone.grid(row=3, column=1)
        tk.Button(self.frame, text="Submit", command=lambda: self.register_user(username.get(), password.get(), email.get(), phone.get())).grid(row=4, column=0, columnspan=2)

    def register_user(self, username, password, email, phone):
        success, message = self.auth.register(username, password, email, phone)
        messagebox.showinfo("Registration", message)
        if success:
            self.clear_frame()
            self.main_menu()

    def login(self):
        self.clear_frame()
        tk.Label(self.frame, text="Username:").grid(row=0, column=0)
        username = tk.Entry(self.frame)
        username.grid(row=0, column=1)
        tk.Label(self.frame, text="Password:").grid(row=1, column=0)
        password = tk.Entry(self.frame, show="*")
        password.grid(row=1, column=1)
        tk.Button(self.frame, text="Submit", command=lambda: self.login_user(username.get(), password.get())).grid(row=2, column=0, columnspan=2)

    def login_user(self, username, password):
        success, message, token = self.auth.login(username, password)
        if success:
            messagebox.showinfo("Login", f"{message}\nYour token is: {token}")
            self.after_login(token)
        else:
            messagebox.showerror("Login", message)
            self.clear_frame()
            self.main_menu()

    def after_login(self, token):
        self.clear_frame()
        tk.Button(self.frame, text="Validate Token", command=lambda: self.validate_token(token)).grid(row=0, column=0)
        tk.Button(self.frame, text="Exit", command=self.exit_app).grid(row=1, column=0)

    def validate_token(self, token):
        valid, username_or_message = self.auth.verify_token(token)
        if valid:
            messagebox.showinfo("Token", f"Token is valid for user: {username_or_message}")
        else:
            messagebox.showerror("Token", username_or_message)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def main_menu(self):
        tk.Button(self.frame, text="Register", command=self.register).grid(row=0, column=0)
        tk.Button(self.frame, text="Login", command=self.login).grid(row=1, column=0)
        tk.Button(self.frame, text="Exit", command=self.exit_app).grid(row=2, column=0)

    def exit_app(self):
        self.db.close()
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()
