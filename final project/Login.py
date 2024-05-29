import tkinter as tk
import sqlite3
from tkinter import messagebox

class LoginApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.create_login_form()

    def create_login_form(self):
        # Create a frame for the login form
        frame = tk.Frame(self.root, bg='#FFFFFF', bd=10)
        frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=300)

        # Title
        label_title = tk.Label(frame, text="Sign In", bg="#000000", fg="white", font=("Arial", 18, 'bold'))
        label_title.pack(pady=10)

        # Username Entry
        self.entry_username = tk.Entry(frame, font=("Arial", 12), relief="flat", bg="white", fg="black")
        self.entry_username.insert(0, "username")
        self.entry_username.bind("<FocusIn>", self.clear_username)
        self.entry_username.pack(pady=10, ipady=5, ipadx=5, fill=tk.X)

        # Password Entry
        self.entry_password = tk.Entry(frame, show='*', font=("Arial", 12), relief="flat", bg="white", fg="black")
        self.entry_password.insert(0, "password")
        self.entry_password.bind("<FocusIn>", self.clear_password)
        self.entry_password.pack(pady=10, ipady=5, ipadx=5, fill=tk.X)

        # Sign Up and Forgot Password Links
        sign_up_label = tk.Label(frame, text="sign up", bg="#000000", fg="blue", font=("Arial", 10), cursor="hand2")
        sign_up_label.pack()
        sign_up_label.bind("<Button-1>", self.sign_up_label)

        # Login
        button_login = tk.Button(frame, text="Login", bg="#FFD700", fg="black", font=("Arial", 12, 'bold'), command=self.Login)
        button_login.pack(pady=10, ipadx=10, ipady=5)

    def clear_username(self, event):
        if self.entry_username.get() == "username":
            self.entry_username.delete(0, tk.END)

    def clear_password(self, event):
        if self.entry_password.get() == "password":
            self.entry_password.delete(0, tk.END)

    def sign_up_label(self, event):
        self.root.destroy()
        import sign_up
        sign_up.main()

    def Login(self):
        con = sqlite3.connect("final_project")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM sign_up_tbl WHERE username = '{self.entry_username.get()}'")
        result = cur.fetchone()
        if result:
            if self.entry_password.get() == result[1]:
                messagebox.showinfo("Success", "Login Succesful.")
                con.close()
                self.root.destroy()
                import choices
                choices.main()
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "User not found.")
        con.close()
def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
