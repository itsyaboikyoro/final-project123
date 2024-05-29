import tkinter as tk

def main():
    window = tk.Tk()
    window.geometry("360x240")

    def emp_info_clicked():
        window.destroy()
        import emp_info
        emp_info.main()

    def payroll_clicked():
        window.destroy()
        import payroll
        payroll.main()

    def user_info_clicked():
        window.destroy()
        import user_info
        user_info.main()

    def sign_out():
        window.destroy()
        import Login
        Login.main()

    emp_info = tk.Button(window, text="emp info", bg="#FFFFFF", fg="black", font=("Arial", 12, 'bold'), command=emp_info_clicked)
    emp_info.place(x=50, y=100)

    payroll = tk.Button(window, text="payroll", bg="#FFFFFF", fg="black", font=("Arial", 12, 'bold'), command=payroll_clicked)
    payroll.place(x=145, y=100)

    user_info = tk.Button(window, text="user info", bg="#FFFFFF", fg="black", font=("Arial", 12, 'bold'), command=user_info_clicked)
    user_info.place(x=225, y=100)

    sign_out = tk.Button(window, text="sign out", bg="#FFFFFF", fg="black", font=("Arial", 12, 'bold'), command=sign_out)
    sign_out.place(x=145, y=150)

    window.mainloop()

if __name__ == "__main__":
    main()