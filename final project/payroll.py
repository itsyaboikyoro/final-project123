import tkinter as tk
from tkinter import *
import sqlite3

class SeRisChoicePayroll:
    def __init__(self, window):
        self.window = window
        self.window.title("Se-ri's Choice Payroll")

        frame = Frame(self.window, width=850, height=800, bg='#d3d3d3')
        frame.place(x=1, y=1)

        self.create_heading(frame)
        self.create_employee_basic_info(frame)
        self.create_income_info(frame)
        self.create_deduction_info(frame)
        self.create_button_info(window)

    def create_heading(self, frame):
        heading = Label(frame, text="SE-RI'S CHOICE PAYROLL", fg='black', bg='#d3d3d3', font=('Algerian', 30, 'bold'))
        heading.place(x=170, y=1)

    def netIncome(self):
        gross = float(self.rhour_basic.get())

        # ---------- SSS Contribution Computation ---------- #
        sss_con, g_var = 180.00, gross

        while sss_con < 900.00 and g_var >= 4250:
            g_var -= 500.00
            sss_con += 22.50

        self.sssc.config(state="normal")
        self.sssc.delete(0, "end")
        self.sssc.insert(0, f"{sss_con}")
        self.sssc.config(state="readonly")

        # ---------- PhilHealth contribution ---------- #
        s_co = self.pd.get().split("/")
        salary_cutoff_year = int(s_co[2])

        if salary_cutoff_year == 2019:
            premium_rate = 0.0275
            upper_value = 50000
        elif salary_cutoff_year == 2020:
            premium_rate = 0.03
            upper_value = 60000
        elif salary_cutoff_year == 2021:
            premium_rate = 0.035
            upper_value = 70000
        elif salary_cutoff_year == 2022:
            premium_rate = 0.04
            upper_value = 80000
        elif salary_cutoff_year == 2023:
            premium_rate = 0.045
            upper_value = 90000
        else:  # for years 2024-2025
            premium_rate = 0.05
            upper_value = 100000

        if gross <= 10000:
            philhealth_con = 10000 * premium_rate
        elif 10000 > gross > upper_value:
            philhealth_con = gross * premium_rate
        else:
            philhealth_con = upper_value * premium_rate

        self.phc.config(state="normal")
        self.phc.delete(0, "end")
        self.phc.insert(0, f"{philhealth_con}")
        self.phc.config(state="readonly")

        # ----------Withholding Tax ---------- #
        if 0.00 < gross <= 10417.00:
            withholding_tax = 0
        elif 10417.00 < gross <= 16666.00:
            over = gross - 10417.00
            withholding_tax = 0 + (over * 0.15)
        elif 16666.00 < gross <= 33332.00:
            over = gross - 16667.00
            withholding_tax = 937.50 + (over * 0.2)
        elif 33332.00 < gross <= 83332.00:
            over = gross - 33333.00
            withholding_tax = 4270.70 + (over * 0.25)
        elif 83332.00 < gross <= 333332.00:
            over = gross - 83333.00
            withholding_tax = 16770.70 + (over * 0.3)
        else:  # for gross pay equal to 333,333 and above
            over = gross - 333333.00
            withholding_tax = 91770.70 + (over * 0.35)

        self.itc.config(state="normal")
        self.itc.delete(0, "end")
        self.itc.insert(0, f"{withholding_tax}")
        self.itc.config(state="readonly")

        self.pgc.config(state="normal")
        self.pgc.delete(0, "end")
        self.pgc.insert(0, "100")
        self.pgc.config(state="readonly")

        deduction = float(sss_con + philhealth_con + withholding_tax + 100)

        deduction += float(self.sssl.get())
        deduction += float(self.pgloan.get())
        deduction += float(self.fcsl.get())
        deduction += float(self.fcsd.get())

        self.totald.config(state="normal")
        self.totald.delete(0, "end")
        self.totald.insert(0, f"{deduction}")
        self.totald.config(state="readonly")
        self.nic.config(state="normal")
        self.nic.delete(0, "end")
        self.nic.insert(0, f"{gross - deduction}")
        self.nic.config(state="readonly")

    def grossIncome(self):
        income_0 = float(self.rhour_basic.get()) * float(self.co_basic.get())
        income_1 = float(self.rhour_honorarium.get()) * float(self.co_honorarium.get())
        income_2 = float(self.rhour_otherincome.get()) * float(self.co_otherincome.get())
        gross_income = income_0 + income_1 + income_2
        self.gic.insert(0, gross_income)
        self.ico_basic.insert(0, income_0)
        self.ico_honorarium.insert(0, income_1)
        self.ico_otherincome.insert(0, income_2)

    def search(self):

        con = sqlite3.connect("final_project")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM payroll_tbl WHERE employee_number = '{self.empno.get()}'")

        info = cur.fetchone()
        print(info)

        self.fn.delete(0, "end")
        self.fn.insert(0, info[1])

        self.mn.delete(0, "end")
        self.mn.insert(0, info[2])

        self.sn.delete(0, "end")
        self.sn.insert(0, info[3])

        self.dept.delete(0, "end")
        self.dept.insert(0, info[9])

        self.cv.delete(0, "end")
        self.cv.insert(0, info[4])

        self.qds.delete(0, "end")
        self.qds.insert(0, info[5])

        self.pd.delete(0, "end")
        self.pd.insert(0, info[6])

        self.emps.delete(0, "end")
        self.emps.insert(0, info[7])

        self.des.delete(0, "end")
        self.des.insert(0, info[8])

        con.close()

    def save_command(self):
        conn = sqlite3.connect('final_project')
        cursor = conn.cursor()

        # Create table if it does not exist
        create_table_query = '''CREATE TABLE IF NOT EXISTS payroll_tbl (
            employee_number TEXT,
            first_name_entry TEXT,
            middle_name_entry TEXT,
            last_name_entry TEXT,
            civil_status_entry TEXT,
            qualified_menu TEXT,
            paydate_entry TEXT,
            emp_stat_entry TEXT,
            designation_entry TEXT,
            department_entry,
            basic_income TEXT,
            honorarium_income TEXT,
            other_income TEXT,
            gross_income TEXT,
            net_entry TEXT,
            total_deduction TEXT
        )'''
        cursor.execute(create_table_query)

        # Extract data from GUI elements
        data = [
            self.empno.get(),
            self.fn.get(),
            self.mn.get(),
            self.sn.get(),
            self.cv.get(),
            self.qds.get(),
            self.pd.get(),
            self.emps.get(),
            self.des.get(),
            self.dept.get(),
            self.ico_basic.get(),
            self.ico_honorarium.get(),
            self.ico_otherincome.get(),
            self.gic.get(),
            self.nic.get(),
            self.totald.get()
        ]

        # Define the SQL query to insert data into the table
        insert_query = '''INSERT INTO payroll_tbl (
            employee_number, first_name_entry, middle_name_entry, last_name_entry, civil_status_entry,
            qualified_menu, paydate_entry, emp_stat_entry, designation_entry, department_entry,
            basic_income, honorarium_income, other_income, gross_income, net_entry, total_deduction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insert_query, data)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Print confirmation message
        print("UPLOADED")

        # Clear the entries (Optional)
        entries = [self.empno, self.fn, self.mn, self.sn, self.cv,
                   self.qds, self.pd,
                   self.emps, self.des, self.dept,
                   self.ico_basic, self.ico_honorarium, self.ico_otherincome, self.gic, self.nic, self.totald]
        for entry in entries:
            entry.delete(0, 'end')

    def update_command(self):
        try:
            conn = sqlite3.connect('final_project')
            cursor = conn.cursor()

            # Extract data from GUI elements
            data = [
                self.fn.get(),
                self.mn.get(),
                self.sn.get(),
                self.cv.get(),
                self.qds.get(),
                self.pd.get(),
                self.emps.get(),
                self.des.get(),
                self.dept.get(),
                self.ico_basic.get(),
                self.ico_honorarium.get(),
                self.ico_otherincome.get(),
                self.gic.get(),
                self.nic.get(),
                self.totald.get(),
                self.empno.get()  # Use employee_number as the key
            ]

            # Define the SQL query to update data into the table
            update_query = '''UPDATE payroll_tbl SET
                first_name_entry =?,
                middle_name_entry =?,
                last_name_entry =?,
                civil_status_entry =?,
                qualified_menu =?,
                paydate_entry =?,
                emp_stat_entry =?,
                designation_entry =?,
                department_entry =?,
                basic_income =?,
                honorarium_income =?,
                other_income =?,
                gross_income =?,
                net_entry =?,
                total_deduction =?
                WHERE employee_number =?'''
            cursor.execute(update_query, data)

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            # Print confirmation message
            print("UPDATED")

            # Clear the entries (Optional)
            entries = [self.empno, self.fn, self.mn, self.sn, self.cv,
                       self.qds, self.pd,
                       self.emps, self.des, self.dept,
                       self.ico_basic, self.ico_honorarium, self.ico_otherincome, self.gic, self.nic, self.totald]
            for entry in entries:
                entry.delete(0, 'end')

        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def new_button(self):
        self.empno.delete(0, "end")
        self.dept.delete(0, "end")
        self.fn.delete(0, "end")
        self.mn.delete(0, "end")
        self.sn.delete(0, "end")
        self.cv.delete(0, "end")
        self.qds.delete(0, "end")
        self.pd.delete(0, "end")
        self.emps.delete(0, "end")
        self.des.delete(0, "end")
        self.rhour_basic.delete(0, "end")
        self.co_basic.delete(0, "end")
        self.ico_basic.delete(0, "end")
        self.rhour_honorarium.delete(0, "end")
        self.co_honorarium.delete(0, "end")
        self.ico_honorarium.delete(0, "end")
        self.rhour_otherincome.delete(0, "end")
        self.ico_otherincome.delete(0, "end")
        self.co_otherincome.delete(0, "end")
        self.gic.delete(0, "end")
        self.nic.delete(0, "end")
        self.sssc.delete(0, "end")
        self.phc.delete(0, "end")
        self.pgc.delete(0, "end")
        self.itc.delete(0, "end")
        self.sssl.delete(0, "end")
        self.pgloan.delete(0, "end")
        self.fcsd.delete(0, "end")
        self.fcsl.delete(0, "end")
        self.totald.delete(0, "end")

    def return_button(self):
        self.window.destroy()
        import choices
        choices.main()
    def create_employee_basic_info(self, frame):
        employeebf = Label(frame, text="EMPLOYEE BASIC INFO:", fg='black', bg='#d3d3d3', font=('Calibri', 10, 'bold'))
        employeebf.place(x=45, y=60)

        border = Label(frame, width=16, height=7, bg="gray", border=2)
        border.place(x=50, y=80)

        employeeno = Label(frame, text="Employee Number:", width=15, bg='#d3d3d3', font=("bold", 10))
        employeeno.place(x=50, y=200)
        self.empno = Entry(frame)
        self.empno.place(x=200, y=200)

        searchemp = Label(frame, text="Search Employee:", width=15, bg='#d3d3d3', font=("bold", 10))
        searchemp.place(x=46, y=230)
        self.button1 = Button(self.window, width=10, text="SEARCH", bg='red', fg='white', font=("Calibri", 10), command=self.search)
        self.button1.place(x=200, y=230)

        department = Label(frame, text="Department:", width=10, bg='#d3d3d3', font=("bold",10))
        department.place(x=49, y=260)
        self.dept = Entry(frame)
        self.dept.place(x=200, y=260)

        firstname = Label(frame, text="First Name: ", width=15, bg='#d3d3d3', font=("bold", 10))
        firstname.place(x=415, y=60)
        self.fn = Entry(frame)
        self.fn.place(x=550, y=60)

        middlename = Label(frame, text="Middle Name: ", width=15, bg='#d3d3d3', font=("bold", 10))
        middlename.place(x=420, y=90)
        self.mn = Entry(frame)
        self.mn.place(x=550, y=90)

        surname = Label(frame, text="Surname: ", width=15, bg='#d3d3d3', font=("bold", 10))
        surname.place(x=408, y=120)
        self.sn = Entry(frame)
        self.sn.place(x=550, y=120)

        civilstatus = Label(frame, text="Civil Status: ", width=15, bg='#d3d3d3', font=("bold", 10))
        civilstatus.place(x=415, y=150)
        self.cv = Entry(frame)
        self.cv.place(x=550, y=150)

        qualds = Label(frame, text="Qualified Dependents\nStatus: ", width=20, bg='#d3d3d3', font=("bold", 8))
        qualds.place(x=408, y=180)
        self.qds = Entry(frame)
        self.qds.place(x=550, y=180)

        paydate = Label(frame, text="Paydate: ", width=15, bg='#d3d3d3', font=("bold", 10))
        paydate.place(x=408, y=210)
        self.pd = Entry(frame)
        self.pd.place(x=550, y=210)

        empstatus = Label(frame, text="Employee Status: ", width=15, bg='#d3d3d3', font=("bold", 10))
        empstatus.place(x=413, y=240)
        self.emps = Entry(frame)
        self.emps.place(x=550, y=240)

        design = Label(frame, text="Designation: ", width=15, bg='#d3d3d3', font=("bold", 10))
        design.place(x=415, y=270)
        self.des = Entry(frame)
        self.des.place(x=550, y=270)

    def create_income_info(self, frame):
        basicincome = Label(frame, text="BASIC INCOME:", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        basicincome.place(x=45, y=290)

        ratehour_basic = Label(frame, text="Rate/Hour:", width=10, bg='#d3d3d3', font=("bold", 10))
        ratehour_basic.place(x=46, y=320)
        self.rhour_basic = Entry(frame)
        self.rhour_basic.place(x=200, y=320)

        cutoff_basic = Label(frame, text="No. of Hours/Cut Off:", width=15, bg='#d3d3d3', font=("bold", 10))
        cutoff_basic.place(x=55, y=350)
        self.co_basic = Entry(frame)
        self.co_basic.place(x=200, y=350)

        incomeco_basic = Label(frame, text="Income/Cut Off:", width=15, bg='#d3d3d3', font=("bold", 10))
        incomeco_basic.place(x=41, y=380)
        self.ico_basic = Entry(frame)
        self.ico_basic.place(x=200, y=380)

        honorariumincome = Label(frame, text="HONORARIUM INCOME:", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        honorariumincome.place(x=45, y=410)

        ratehour_honorarium = Label(frame, text="Rate/Hour:", width=10, bg='#d3d3d3', font=("bold", 10))
        ratehour_honorarium.place(x=46, y=440)
        self.rhour_honorarium = Entry(frame)
        self.rhour_honorarium.place(x=200, y=440)

        cutoff_honorarium = Label(frame, text="No. of Hours/Cut Off: ", width=15, bg='#d3d3d3', font=("bold", 10))
        cutoff_honorarium.place(x=55, y=470)
        self.co_honorarium = Entry(frame)
        self.co_honorarium.place(x=200, y=470)

        incomeco_honorarium = Label(frame, text="Income/Cut Off: ", width=15, bg='#d3d3d3', font=("bold", 10))
        incomeco_honorarium.place(x=41, y=500)
        self.ico_honorarium = Entry(frame)
        self.ico_honorarium.place(x=200, y=500)

        otherincome = Label(frame, text="OTHER INCOME: ", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        otherincome.place(x=45, y=530)

        ratehour_otherincome = Label(frame, text="Rate/Hour:", width=10, bg='#d3d3d3', font=("bold", 10))
        ratehour_otherincome.place(x=46, y=560)
        self.rhour_otherincome = Entry(frame)
        self.rhour_otherincome.place(x=200, y=560)

        cutoff_otherincome = Label(frame, text="No. of Hours/Cut Off: ", width=15, bg='#d3d3d3', font=("bold", 10))
        cutoff_otherincome.place(x=55, y=590)
        self.co_otherincome = Entry(frame)
        self.co_otherincome.place(x=200, y=590)

        incomeco_otherincome = Label(frame, text="Income/Cut Off: ", width=15, bg='#d3d3d3', font=("bold", 10))
        incomeco_otherincome.place(x=41, y=620)
        self.ico_otherincome = Entry(frame)
        self.ico_otherincome.place(x=200, y=620)

        summaryincome = Label(frame, text="SUMMARY INCOME: ", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        summaryincome.place(x=45, y=650)

        grossincome = Label(frame, text="Rate/Hour:", width=10, bg='#d3d3d3', font=("bold", 10))
        grossincome.place(x=46, y=680)
        self.gic = Entry(frame)
        self.gic.place(x=200, y=680)

        netincome = Label(frame, text="No. of Hours/Cut Off: ", width=15, bg='#d3d3d3', font=("bold", 10))
        netincome.place(x=55, y=710)
        self.nic = Entry(frame)
        self.nic.place(x=200, y=710)

    def create_deduction_info(self, frame):
        regded = Label(frame, text="REGULAR DEDUCTIONS: ", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        regded.place(x=415,y=290)
        ssscon = Label(frame, text="SSS Contribution: ", width=15, bg='#d3d3d3', font=("bold",10))
        ssscon.place(x=415, y=320)
        self.sssc = Entry(frame)
        self.sssc.place(x=550, y=320)

        phcon = Label(frame, text="PhilHealth Contribution: ", width=18, bg='#d3d3d3', font=("bold", 10))
        phcon.place(x=410, y=350)
        self.phc = Entry(frame)
        self.phc.place(x=550, y=350)

        pagcon = Label(frame, text="Pagibig Contribution: ", width=15, bg='#d3d3d3', font=("bold", 10))
        pagcon.place(x=420, y=380)
        self.pgc = Entry(frame)
        self.pgc.place(x=550, y=380)

        inctaxc = Label(frame, text="Income Tax Contribution: ", width=18, bg='#d3d3d3', font=("bold", 10))
        inctaxc.place(x=408, y=410)
        self.itc = Entry(frame)
        self.itc.place(x=550, y=410)

        otherded = Label(frame, text="OTHER DEDUCTIONS: ", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        otherded.place(x=415, y=440)

        sssloan = Label(frame, text="SSS Loan: ", width=15, bg='#d3d3d3', font=("bold", 10))
        sssloan.place(x=407, y=470)
        self.sssl = Entry(frame)
        self.sssl.place(x=550, y=470)

        pagloan = Label(frame, text="Pagibig Loan: ", width=15, bg='#d3d3d3', font=("bold", 10))
        pagloan.place(x=415, y=500)
        self.pgloan = Entry(frame)
        self.pgloan.place(x=550, y=500)

        fcsdep = Label(frame, text="Faculty Savings\nDeposit: ", width=15, bg='#d3d3d3', font=("bold", 8))
        fcsdep.place(x=415, y=530)
        self.fcsd = Entry(frame)
        self.fcsd.place(x=550, y=530)

        fcsloan = Label(frame, text="Faculty Savings Loan: ", width=20, bg='#d3d3d3', font=("bold", 8))
        fcsloan.place(x=415, y=560)
        self.fcsl = Entry(frame)
        self.fcsl.place(x=550, y=560)

        dedsum = Label(frame, text="DEDUCTION SUMMARY: ", fg='black', bg='#d3d3d3', font=('Calibri', 15, 'bold'))
        dedsum.place(x=415, y=590)

        totalded = Label(frame, text="Total Deductions: ", width=15, bg='#d3d3d3', font=("bold", 10))
        totalded.place(x=407, y=620)
        self.totald = Entry(frame)
        self.totald.place(x=550, y=620)

    def create_button_info(self, window):
        button2 = Button(window, width=11, text="GROSS INCOME", bg='blue', fg='white', font=("Calibri", 10), command=self.grossIncome)
        button2.place(x=415, y=650)

        button3 = Button(window, width=10, text="NET INCOME", bg='blue', fg='white', font=("Calibri", 10), command=self.netIncome)
        button3.place(x=505, y=650)

        button4 = Button(window, width=10, text="SAVE", bg='#009966', fg='white', font=("Calibri", 10), command=self.save_command)
        button4.place(x=587, y=650)

        button5 = Button(window, width=10, text="UPDATE", bg='#009966', fg='white', font=("Calibri", 10), command=self.update_command)
        button5.place(x=670, y=650)

        button6 = Button(window, width=10, text="NEW", bg='#FFAE42', fg='white', font=("Calibri", 10), command=self.new_button)
        button6.place(x=755, y=650)

        button7 = Button(window, width=10, text="RETURN", bg='#FFFFFF', fg='black', font=("Calibri", 10), command=self.return_button)
        button7.place(x=587, y=675)

        self.window.geometry("850x800")
        self.window.mainloop()

def main():
    window = tk.Tk()
    SeRisChoicePayroll(window)
    window.mainloop()

if __name__ == "__main__":
    main()