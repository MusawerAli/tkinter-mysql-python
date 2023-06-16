import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
import csv
import mysql.connector


# Create a MySQL connection
cnx = mysql.connector.connect(
    host='localhost',
    user='phpmyadmin',
    password='Root!123',
    database='test1'
)

class BankAccount:
    def __init__(self,id,name,account_number,pin,balance,is_admin=False,):
        self.id = id
        self.name = name
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.is_admin = is_admin
        self.transaction_history = []

    def check_balance(self):
        return self.balance

    def withdraw(self, amount,id):
        if amount <= self.balance:
            self.balance -= amount
            cursor = cnx.cursor()
            query = "INSERT INTO transition (amount,type, user_id) VALUES (%s, %s, %s)"
            data = (amount, "withdraw", id)
            cursor.execute(query, data)
            select_query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(select_query, (id,))
            record = cursor.fetchone()
            if record is not None:
                balance = record[5]
                balance = balance - amount
                update_query = "UPDATE users SET balance = %s WHERE id = %s"
                update_values = (balance, id)
                cursor.execute(update_query, update_values)
            cnx.commit()
            cursor.close()
            # self.transaction_history.append(f"Withdraw: ${amount}")
            return True
        else:
            return False
    
    def deposit(self, amount,id):
        self.balance += amount
        cursor = cnx.cursor()
        query = "INSERT INTO transition (amount,type, user_id) VALUES (%s, %s, %s)"
        data = (amount, "deposit", id)
        cursor.execute(query, data)
        select_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(select_query, (id,))
        record = cursor.fetchone()
        if record is not None:
            balance = record[5]
            balance = balance + amount
            update_query = "UPDATE users SET balance = %s WHERE id = %s"
            update_values = (balance, id)
            cursor.execute(update_query, update_values)
        cnx.commit()
        cursor.close()
        # self.transaction_history.append(f"Deposit: ${amount}")
        return True

    def get_transaction_history(self):
        cursor = cnx.cursor()
        select_query = "SELECT * FROM transition WHERE user_id = %s"
        cursor.execute(select_query, (self.id,))
        record = cursor.fetchall()
        if record is not None:
            result_list = []
            column_names = cursor.column_names
            for row in record:
                result_dict = {}
                for i, column_value in enumerate(row):
                    result_dict[column_names[i]] = column_value
                result_list.append(result_dict)
            return result_list
        return None
    
    @staticmethod
    def get_users(account_number, pin):
        cursor = cnx.cursor()
        query = "SELECT * FROM users WHERE account_number = %s AND pin = %s"
        cursor.execute(query, (account_number, pin))
        result = cursor.fetchone()
        cursor.close()

        if result:
            id=result[0]
            name=result[1]
            account_number=result[2] 
            pin=result[3]
            is_admin=result[4]
            balance=result[5]
            return BankAccount(id,name,account_number, pin,balance,is_admin)
        else:
            return None
        
        
        

class ATMGUI:
    def __init__(self):
        # self.accounts = []
        # self.accounts.append(BankAccount("admin", "admin123", 0, is_admin=True))  # Admin hesabı
        # self.accounts.append(BankAccount("123456789", "1234", 5000))  # Standart hesap
        self.current_user = None

        self.root = tk.Tk()
        self.root.title("ATM")

        self.intro_label = tk.Label(self.root, text="Welcome to the ATM")
        self.intro_label.pack(pady=20)

        self.account_frame = tk.Frame(self.root)

        self.account_number_label = tk.Label(self.account_frame, text="Account Number:")
        self.account_number_label.grid(row=0, column=0)
        self.account_number_entry = tk.Entry(self.account_frame)
        self.account_number_entry.grid(row=0, column=1)

        self.name_label = tk.Label(self.account_frame, text="Name:")
        self.name_label.grid(row=1, column=0)
        self.name_entry = tk.Entry(self.account_frame, show="*")
        self.name_entry.grid(row=1, column=1)

        self.pin_label = tk.Label(self.account_frame, text="PIN:")
        self.pin_label.grid(row=1, column=0)
        self.pin_entry = tk.Entry(self.account_frame, show="*")
        self.pin_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.account_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.balance_label = tk.Label(self.root, text="")
        self.withdraw_button = tk.Button(self.root, text="Withdraw", command=self.open_withdraw_popup)
        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.open_deposit_popup)
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)

        self.account_frame.pack()

        self.root.mainloop()

    def login(self):
        account_number = self.account_number_entry.get()
        pin = self.pin_entry.get()
        account = BankAccount.get_users(account_number, pin)
        if account:
            self.current_user = account
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid account number or PIN!")
        # for account in self.accounts:
        #     if account.account_number == account_number and account.pin == pin:
        #         self.current_user = account
        #         self.show_main_menu()
        #         return
        # messagebox.showerror("Error", "Invalid account number or PIN!")

    def show_main_menu(self):
        self.intro_label.pack_forget()
        self.account_frame.pack_forget()

        self.balance_label.config(text="Balance: $%.2f" % self.current_user.check_balance())
        self.balance_label.pack(pady=10)
        self.withdraw_button.pack(pady=5)
        self.deposit_button.pack(pady=5)
        self.logout_button.pack(pady=10)

        if self.current_user.is_admin:
            self.add_user_button = tk.Button(self.root, text="Add User", command=self.open_add_user_popup)
            self.add_user_button.pack(pady=5)

            self.transaction_history_button = tk.Button(self.root, text="Transaction History",
                                                        command=self.open_transaction_history_popup)
            self.transaction_history_button.pack(pady=5)

    def open_withdraw_popup(self):
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Withdraw")

        withdraw_label = tk.Label(withdraw_window, text="Enter withdrawal amount:")
        withdraw_label.pack(pady=10)

        amount_entry = tk.Entry(withdraw_window)
        amount_entry.pack()

        withdraw_button = tk.Button(withdraw_window, text="Withdraw",
                                    command=lambda: self.withdraw(amount_entry.get(), withdraw_window))
        withdraw_button.pack(pady=5)

    def withdraw(self, amount, withdraw_window):
        amount = float(amount)
        if self.current_user.withdraw(amount,self.current_user.id):
            messagebox.showinfo("Success", "Withdrawal successful!")
            self.balance_label.config(text="Balance: $%.2f" % self.current_user.check_balance())
        else:
            messagebox.showerror("Error", "Insufficient balance!")
        withdraw_window.destroy()

    def open_deposit_popup(self):
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit")

        deposit_label = tk.Label(deposit_window, text="Enter deposit amount:")
        deposit_label.pack(pady=10)

        amount_entry = tk.Entry(deposit_window)
        amount_entry.pack()

        deposit_button = tk.Button(deposit_window, text="Deposit",
                                   command=lambda: self.deposit(amount_entry.get(), deposit_window))
        deposit_button.pack(pady=5)

    def deposit(self, amount, deposit_window):
        amount = float(amount)
        self.current_user.deposit(amount,self.current_user.id)
        messagebox.showinfo("Success", "Deposit successful!")
        self.balance_label.config(text="Balance: $%.2f" % self.current_user.check_balance())
        deposit_window.destroy()

    def logout(self):
        self.current_user = None

        self.balance_label.pack_forget()
        self.withdraw_button.pack_forget()
        self.deposit_button.pack_forget()
        self.logout_button.pack_forget()

        if hasattr(self, 'add_user_button'):
            self.add_user_button.pack_forget()

        if hasattr(self, 'transaction_history_button'):
            self.transaction_history_button.pack_forget()

        self.intro_label.pack()
        self.account_frame.pack()

    def open_add_user_popup(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add User")

        account_number_label = tk.Label(add_user_window, text="Account Number:")
        account_number_label.pack(pady=10)

        account_number_entry = tk.Entry(add_user_window)
        account_number_entry.pack()

        name_label = tk.Label(add_user_window, text="Name:")
        name_label.pack()

        name_entry = tk.Entry(add_user_window)
        name_entry.pack()

        pin_label = tk.Label(add_user_window, text="PIN:")
        pin_label.pack()

        pin_entry = tk.Entry(add_user_window, show="*")
        pin_entry.pack()

        balance_label = tk.Label(add_user_window, text="Initial Balance:")
        balance_label.pack()

        balance_entry = tk.Entry(add_user_window)
        balance_entry.pack()

        add_user_button = tk.Button(add_user_window, text="Add User",
                                    command=lambda: self.add_user(account_number_entry.get(),name_entry.get(), pin_entry.get(),
                                                                  balance_entry.get(), add_user_window))
        add_user_button.pack(pady=10)

    def add_user(self, account_number,name, pin, balance, add_user_window):
        balance = float(balance)
        is_admin = False
        name = name
        account_number = account_number
        cursor = cnx.cursor()
        query = "INSERT INTO users (name,account_number, pin,is_admin,balance) VALUES (%s, %s, %s, %s, %s)"
        data = (name, account_number,pin,is_admin,balance)
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        # self.accounts.append(BankAccount(name,account_number, pin, balance, is_admin))
        messagebox.showinfo("Success", "User added successfully!")
        add_user_window.destroy()

    def open_transaction_history_popup(self):
        transaction_history_window = tk.Toplevel(self.root)
        transaction_history_window.title("Transaction History")

        transaction_history_label = tk.Label(transaction_history_window, text="Transaction History")
        transaction_history_label.pack(pady=10)

        treeview = ttk.Treeview(transaction_history_window)
        treeview["columns"] = ("id",'amount','type')

        treeview.column("id", width=50, minwidth=50, stretch=tk.NO)
        treeview.column("amount", width=80, minwidth=80, stretch=tk.NO)
        treeview.column("type", width=100, minwidth=100, stretch=tk.NO)        

        treeview.heading("id", text="id.", anchor=tk.W)
        treeview.heading("amount", text="amount", anchor=tk.W)
        treeview.heading("type", text="type", anchor=tk.W)
        

        for index, transaction in enumerate(self.current_user.get_transaction_history()):
            treeview.insert(parent="", index=index, iid=index, values=(transaction['id'], transaction['amount'],transaction['type']))

        treeview.pack()

        export_button = tk.Button(transaction_history_window, text="Export as CSV",
                                  command=lambda: self.export_transaction_history_csv(transaction_history_window))
        export_button.pack(pady=10)

    def export_transaction_history_csv(self, transaction_history_window):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["No.", "Transaction"])
                for index, transaction in enumerate(self.current_user.get_transaction_history()):
                    writer.writerow([index + 1, transaction])
            messagebox.showinfo("Success", "Transaction history exported as CSV successfully!")
        transaction_history_window.destroy()


# Programı başlat
app = ATMGUI()
