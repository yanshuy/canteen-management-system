import tkinter as tk
from tkinter import messagebox

accounts = {
    "yanshuman": {"password": "pass1", "balance": 1000},
    "sanjay": {"password": "pass2", "balance": 2000},
}

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("400x300")
        
        # Create frames
        self.login_frame = tk.Frame(root)
        self.dashboard_frame = tk.Frame(root)
        
        # Initialize login UI
        self.setup_login_ui()
        
        # Show login frame initially
        self.login_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
    def setup_login_ui(self):
        # Username row
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky='e', pady=5)
        self.username_entry = tk.Entry(self.login_frame, width=20)
        self.username_entry.grid(row=0, column=1, pady=5)
        
        # Password row
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky='e', pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", width=20)
        self.password_entry.grid(row=1, column=1, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self.login_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        buttons = [
            ("Login", self.login),
            ("Create Account", self.create_account),
            ("Delete Account", self.delete_account),
            ("List Users", self.list_users),
            ("Exit", self.root.quit)
        ]
        
        # Create buttons in a grid (2 columns)
        for i, (text, command) in enumerate(buttons):
            row, col = divmod(i, 2)
            tk.Button(btn_frame, text=text, command=command, width=12).grid(
                row=row, column=col, padx=5, pady=5
            )
    
    def setup_dashboard_ui(self, username):
        # Clear previous widgets
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        
        # Account info
        tk.Label(self.dashboard_frame, text=f"Balance: ${accounts[username]['balance']}").pack(pady=10)
        
        # Amount entry
        tk.Label(self.dashboard_frame, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.dashboard_frame, width=20)
        self.amount_entry.pack(pady=5)
        
        # Transaction buttons
        btn_frame = tk.Frame(self.dashboard_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Deposit", width=10, 
                 command=lambda: self.deposit(username)).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Withdraw", width=10, 
                 command=lambda: self.withdraw(username)).grid(row=0, column=1, padx=5)
        
        # Logout button
        tk.Button(self.dashboard_frame, text="Logout", width=10,
                 command=self.logout).pack(pady=10)
    
    # Action methods
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in accounts and accounts[username]["password"] == password:
            self.login_frame.pack_forget()
            self.setup_dashboard_ui(username)
            self.dashboard_frame.pack(padx=10, pady=10, fill='both', expand=True)
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password required")
            return
            
        if username in accounts:
            messagebox.showerror("Error", "Account already exists")
        else:
            accounts[username] = {"password": password, "balance": 0}
            messagebox.showinfo("Success", "Account created successfully")
    
    def delete_account(self):
        username = self.username_entry.get()
        
        if username in accounts:
            del accounts[username]
            messagebox.showinfo("Success", "Account deleted successfully")
        else:
            messagebox.showerror("Error", "Account does not exist")
    
    def list_users(self):
        users = "\n".join(accounts.keys())
        messagebox.showinfo("Users", f"Registered Users:\n{users}")
    
    def deposit(self, username):
        try:
            amount = int(self.amount_entry.get())
            accounts[username]["balance"] += amount
            self.setup_dashboard_ui(username)  # Refresh to show new balance
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def withdraw(self, username):
        try:
            amount = int(self.amount_entry.get())
            if amount <= accounts[username]["balance"]:
                accounts[username]["balance"] -= amount
                self.setup_dashboard_ui(username)  # Refresh to show new balance
            else:
                messagebox.showerror("Error", "Insufficient balance")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def logout(self):
        self.dashboard_frame.pack_forget()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.login_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()