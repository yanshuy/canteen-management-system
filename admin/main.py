import tkinter as tk
from dashboard import Dashboard

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("1200x700")
    root.minsize(900, 600)
    
    # Create and pack the dashboard
    dashboard = Dashboard(root)
    dashboard.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

