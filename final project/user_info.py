import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import sqlite3

def main():
    window = tk.Tk()
    window.title("User Account Information")
    app = UserApp(window)
    window.geometry('1250x500')
    window.mainloop()

class UserApp:
    def __init__(self, root):
        self.user_info = UserInfo(root)

class UserInfo:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, width=1200, height=450, bg='light gray')
        self.frame.place(x=20, y=20)

        # First Name
        self.pic_frame = tk.LabelFrame(self.parent, text="")
        self.pic_frame.place(relx=0.175, rely=0.18, anchor="e")

        self.pic1_frame = tk.Frame(self.pic_frame)
        self.pic1_frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        default_image = Image.open("no_profile_pic.jpg")
        default_image = default_image.resize((130, 130))
        default_photo = ImageTk.PhotoImage(default_image)
        self.image_label = tk.Label(self.pic1_frame, image=default_photo)
        self.image_label.grid(row=0, column=0, sticky="w")

        self.first_name_label = Label(self.frame, text='First Name:', bg='light gray', font=('Arial', 11, 'bold'))
        self.first_name_label.place(x=250, y=70)
        self.fn = Entry(self.frame, width=15, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.fn.place(x=250, y=100)

        # Middle Name
        self.middle_name_label = Label(self.frame, text='Middle Name:', bg='light gray', font=('Arial', 11, 'bold'))
        self.middle_name_label.place(x=390, y=70)
        self.mn = Entry(self.frame, width=20, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.mn.place(x=390, y=100)

        # Last Name
        self.last_name_label = Label(self.frame, text='Last Name:', bg='light gray', font=('Arial', 11, 'bold'))
        self.last_name_label.place(x=570, y=70)
        self.ln = Entry(self.frame, width=15, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.ln.place(x=570, y=100)

        # Suffix
        self.suffix_label = Label(self.frame, text='Suffix:', bg='light gray', font=('Arial', 11, 'bold'))
        self.suffix_label.place(x=710, y=70)
        self.suffix = Entry(self.frame, width=15, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.suffix.place(x=710, y=100)

        # Department
        self.department_label = Label(self.frame, text='Department:', bg='light gray', font=('Arial', 11, 'bold'))
        self.department_label.place(x=850, y=70)
        self.dept = Entry(self.frame, width=30, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.dept.place(x=850, y=100)

        # Designation
        self.designation_label = Label(self.frame, text='Designation:', bg='light gray', font=('Arial', 11, 'bold'))
        self.designation_label.place(x=50, y=170)
        self.designation = Entry(self.frame, width=40, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.designation.place(x=50, y=200)

        # Username
        self.username_label = Label(self.frame, text='Username:', bg='light gray', font=('Arial', 11, 'bold'))
        self.username_label.place(x=390, y=170)
        self.username = Entry(self.frame, width=30, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.username.place(x=390, y=200)

        # Password
        self.password_label = Label(self.frame, text='Password:', bg='light gray', font=('Arial', 11, 'bold'))
        self.password_label.place(x=650, y=170)
        self.password = Entry(self.frame, width=45, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'),
                              show='*')
        self.password.place(x=650, y=200)

        # Confirm Password
        self.confirm_password_label = Label(self.frame, text='Confirm Password:', bg='light gray',
                                            font=('Arial', 11, 'bold'))
        self.confirm_password_label.place(x=50, y=270)
        self.confirm_password = Entry(self.frame, width=40, fg='black', border=2, bg='white',
                                      font=('Arial', 11, 'bold'), show='*')
        self.confirm_password.place(x=50, y=300)

        # User Type
        self.user_type_label = Label(self.frame, text='User Type:', bg='light gray', font=('Arial', 11, 'bold'))
        self.user_type_label.place(x=390, y=270)
        self.user_type = Entry(self.frame, width=30, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.user_type.place(x=390, y=300)

        # User Status
        self.user_status_label = Label(self.frame, text='User Status:', bg='light gray', font=('Arial', 11, 'bold'))
        self.user_status_label.place(x=650, y=270)
        self.user_status = Entry(self.frame, width=25, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.user_status.place(x=650, y=300)

        # Employee Number
        self.employee_number_label = Label(self.frame, text='Employee Number:', bg='light gray',
                                           font=('Arial', 11, 'bold'))
        self.employee_number_label.place(x=870, y=270)
        self.employee_number = Entry(self.frame, width=30, fg='black', border=2, bg='white', font=('Arial', 11, 'bold'))
        self.employee_number.place(x=870, y=300)

        # Buttons section
        self.update_button = Button(self.frame, width=25, pady=7, text='Update', bg='blue', fg='white', cursor='hand2',border=1, command=self.update_command)
        self.update_button.place(x=200, y=370)

        self.delete_button = Button(self.frame, width=25, pady=7, text='Delete', bg='orange', fg='black', cursor='hand2', border=1, command=self.delete_button)
        self.delete_button.place(x=390, y=370)

        self.cancel_button = Button(self.frame, width=25, pady=7, text='Cancel', bg='light gray', fg='black',cursor='hand2', border=1, command=self.cancel)
        self.cancel_button.place(x=580, y=370)
        self.save_button = Button(self.frame, width=25, pady=7, text='Save', bg='green', fg='white', cursor='hand2',border=1, command=self.save_command)
        self.save_button.place(x=770, y=370)

        self.select_picture = Button(self.frame, width=20, pady=2, text='select photo', bg='white', fg='black', cursor='hand2',border=1, command=self.select_image)
        self.select_picture.place(x=50, y=145)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((130, 130))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
    def save_command(self):
        con = sqlite3.connect('final_project')
        cursor = con.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS user_info_tbl (First_name TEXT,Middle_name TEXT,Last_name TEXT,Suffix TEXT, Department TEXT,Designation TEXT,Username TEXT,Password TEXT,Confirm_Password TEXT,User_type TEXT,User_Status TEXT,Employee_number TEXT)'''
        cursor.execute(create_table_query)

        # Extract data from GUI elements
        data = [
            self.fn.get(),
            self.mn.get(),
            self.ln.get(),
            self.suffix.get(),
            self.dept.get(),
            self.designation.get(),
            self.username.get(),
            self.password.get(),
            self.confirm_password.get(),
            self.user_type.get(),
            self.user_status.get(),
            self.employee_number.get()
        ]

        # Define the SQL query to insert data into the table
        insert_query = '''INSERT INTO user_info_tbl (First_name, Middle_name, Last_name, Suffix, Department, Designation, Username, Password, Confirm_Password, User_type, User_Status, Employee_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insert_query, data)

        # Commit changes and close the connection
        con.commit()
        con.close()
        entries = [self.fn, self.mn, self.ln, self.suffix, self.dept,
                   self.designation, self.username, self.password, self.confirm_password,
                   self.user_type, self.user_status, self.employee_number]

        print("UPLOADED")

        self.fn.delete(0, "end")
        self.mn.delete(0, "end")
        self.ln.delete(0, "end")
        self.suffix.delete(0, "end")
        self.dept.delete(0, "end")
        self.designation.delete(0, "end")
        self.username.delete(0, "end")
        self.password.delete(0, "end")
        self.confirm_password.delete(0, "end")
        self.user_type.delete(0, "end")
        self.user_status.delete(0, "end")
        self.employee_number.delete(0, "end")

    def update_command(self):
        try:
            conn = sqlite3.connect('final_project')
            cursor = conn.cursor()

            # Extract data from GUI elements
            data = [
                self.fn.get(),
                self.mn.get(),
                self.ln.get(),
                self.suffix.get(),
                self.dept.get(),
                self.designation.get(),
                self.username.get(),
                self.password.get(),
                self.confirm_password.get(),
                self.user_type.get(),
                self.user_status.get(),
                self.employee_number.get()
            ]

            # Define the SQL query to update data into the table
            update_query = '''UPDATE user_info_tbl SET
                First_name =?, 
                Middle_name =?, 
                Last_name =?, 
                Suffix =?, 
                Department =?, 
                Designation =?, 
                Username =?, 
                Password =?, 
                Confirm_Password =?, 
                User_type =?, 
                User_Status =?, 
                WHERE Employee_number =?'''
            cursor.execute(update_query, data)

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            # Print confirmation message
            print("UPDATED")

            # Clear the entries (Optional)
            entries = [self.fn, self.mn, self.ln, self.suffix, self.dept, self.designation, self.username, self.password, self.confirm_password, self.user_type, self.user_status, self.employee_number]
            for entry in entries:
                entry.delete(0, 'end')

        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def delete_button(self):
        self.fn.delete(0, "end")
        self.mn.delete(0, "end")
        self.ln.delete(0, "end")
        self.suffix.delete(0, "end")
        self.dept.delete(0, "end")
        self.designation.delete(0, "end")
        self.username.delete(0, "end")
        self.password.delete(0, "end")
        self.confirm_password.delete(0, "end")
        self.user_type.delete(0, "end")
        self.user_status.delete(0, "end")
        self.employee_number.delete(0, "end")

    def cancel(self):
        self.parent.destroy()
        import choices
        choices.main()


if __name__ == "__main__":
    main()