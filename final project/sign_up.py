import tkinter as tk
from tkinter import messagebox
import sqlite3

class SignUpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up Page")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.create_sign_up_form()

    def create_sign_up_form(self):
        # Create a frame for the sign up form
        frame = tk.Frame(self.root, bg='#000000', bd=10)
        frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=300)

        # Title
        label_title = tk.Label(frame, text="Sign Up", bg="#000000", fg="black", font=("Arial", 18, 'bold'))
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

        # Confirm Password Entry
        self.entry_confirm_password = tk.Entry(frame, show='*', font=("Arial", 12), relief="flat", bg="white", fg="black")
        self.entry_confirm_password.insert(0, "confirm password")
        self.entry_confirm_password.bind("<FocusIn>", self.clear_confirm_password)
        self.entry_confirm_password.pack(pady=10, ipady=5, ipadx=5, fill=tk.X)

        # Sign Up and Return Links
        return_label = tk.Label(frame, text="return", bg="#000000", fg="blue", font=("Arial", 10), cursor="hand2")
        return_label.pack()
        return_label.bind("<Button-1>", self.return_label)

        # Sign Up
        button_sign_up = tk.Button(frame, text="Sign Up", bg="#FFD700", fg="black", font=("Arial", 12, 'bold'), command=self.sign_up_clicked)
        button_sign_up.pack(pady=10, ipadx=10, ipady=5)

    def clear_username(self, event):
        if self.entry_username.get() == "username":
            self.entry_username.delete(0, tk.END)

    def clear_password(self, event):
        if self.entry_password.get() == "password":
            self.entry_password.delete(0, tk.END)

    def clear_confirm_password(self, event):
        if self.entry_confirm_password.get() == "confirm password":
            self.entry_confirm_password.delete(0, tk.END)

    def return_label(self, event):
        self.root.destroy()
        import Login
        Login.main()

    def sign_up_clicked(self):
        # Get the sign up information from the input fields
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        # Validate the input values
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Save the data to the database
        con = sqlite3.connect('final_project')
        cursor = con.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS sign_up_tbl (username TEXT, password TEXT, confirm_password TEXT)'''
        cursor.execute(create_table_query)

        # Check if the username already exists
        select_query = '''SELECT * FROM sign_up_tbl WHERE username=?'''
        cursor.execute(select_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "The username is already taken. Please choose another one.")
            con.close()
            return

        # Extract data from GUI elements
        data = [
            username,
            password,
            confirm_password
        ]

        # Define the SQL query to insert data into the table
        insert_query = '''INSERT INTO sign_up_tbl (username, password, confirm_password) VALUES (?, ?, ?)'''
        cursor.execute(insert_query, data)

        # Commit changes and close the connection
        con.commit()
        con.close()

        # Clear the input fields
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_confirm_password.delete(0, tk.END)

        # Display a success message
        messagebox.showinfo("Success", "Sign up successful!")

def main():
    root = tk.Tk()
    app = SignUpApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
