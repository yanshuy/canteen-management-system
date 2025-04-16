import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.colors import COLORS
from utils.widgets import Card

class OrdersPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.parent = parent
        
        # Initialize data
        self.orders = []
        self.status_options = ["New", "Preparing", "Prepared", "Delivered", "Cancelled"]
        
        # Setup UI
        self.setup_header()
        self.setup_content()
        self.setup_footer()
        
        # Load sample data
        self.load_sample_orders()
        
    def setup_header(self):
        """Setup the header section with title and filters"""
        self.header = tk.Frame(self, bg=COLORS["bg_main"], height=70)
        self.header.pack(fill=tk.X)
        
        # Title
        self.title = tk.Label(
            self.header,
            text="Order Management",
            font=("Helvetica", 24, "bold"),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"]
        )
        self.title.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Filter controls
        filter_frame = tk.Frame(self.header, bg=COLORS["bg_main"])
        filter_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(filter_frame, text="Filter by:", bg=COLORS["bg_main"]).pack(side=tk.LEFT)
        
        self.status_filter = ttk.Combobox(
            filter_frame, 
            values=["All"] + self.status_options,
            state="readonly",
            width=15
        )
        self.status_filter.current(0)
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.bind("<<ComboboxSelected>>", self.filter_orders)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.search_orders)
        
    def setup_content(self):
        """Setup the main content area with orders table"""
        self.content = tk.Frame(self, bg=COLORS["bg_main"])
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create orders table
        self.create_orders_table()
        
    def create_orders_table(self):
        """Create and configure the orders Treeview"""
        columns = ("Order ID", "Customer", "Items", "Total", "Status", "Time")
        
        self.tree = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            selectmode="extended",
            height=15
        )
        
        # Configure columns
        self.tree.heading("Order ID", text="Order ID", anchor=tk.CENTER)
        self.tree.heading("Customer", text="Customer", anchor=tk.CENTER)
        self.tree.heading("Items", text="Items", anchor=tk.CENTER)
        self.tree.heading("Total", text="Total", anchor=tk.CENTER)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)
        self.tree.heading("Time", text="Time", anchor=tk.CENTER)
        
        self.tree.column("Order ID", width=100, anchor=tk.CENTER)
        self.tree.column("Customer", width=150, anchor=tk.CENTER)
        self.tree.column("Items", width=200, anchor=tk.CENTER)
        self.tree.column("Total", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=120, anchor=tk.CENTER)
        self.tree.column("Time", width=120, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click event
        self.tree.bind("<Double-1>", self.show_order_details)
        
    def setup_footer(self):
        """Setup the footer with action buttons"""
        footer = tk.Frame(self, bg=COLORS["bg_main"], height=60)
        footer.pack(fill=tk.X, padx=20, pady=10)
        
        # Status update controls
        status_frame = tk.Frame(footer, bg=COLORS["bg_main"])
        status_frame.pack(side=tk.LEFT)
        
        tk.Label(status_frame, text="Update Status:", bg=COLORS["bg_main"]).pack(side=tk.LEFT)
        
        self.new_status = ttk.Combobox(
            status_frame,
            values=self.status_options,
            state="readonly",
            width=12
        )
        self.new_status.current(0)
        self.new_status.pack(side=tk.LEFT, padx=5)
        
        update_btn = tk.Button(
            status_frame,
            text="Apply",
            command=self.update_selected_orders,
            bg=COLORS["primary"],
            fg="white"
        )
        update_btn.pack(side=tk.LEFT)
        
        # Other action buttons
        action_frame = tk.Frame(footer, bg=COLORS["bg_main"])
        action_frame.pack(side=tk.RIGHT)
        
        refresh_btn = tk.Button(
            action_frame,
            text="Refresh",
            command=self.refresh_orders,
            bg=COLORS["secondary"],
            fg="white"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Use get() method with a fallback color in case "success" is still not defined
        success_color = COLORS.get("success", COLORS["secondary"])
        
        add_btn = tk.Button(
            action_frame,
            text="Add Order",
            command=self.add_new_order,
            bg=success_color,
            fg="white"
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
    def load_sample_orders(self):
        """Load sample order data"""
        self.orders = [
            {
                "id": 1001,
                "customer": "Vaibhav Sharma",
                "items": [{"name": "Pizza", "qty": 2}, {"name": "Soda", "qty": 1}],
                "total": 25.98,
                "status": "New",
                "time": "10:30 AM"
            },
            {
                "id": 1002,
                "customer": "From Nashik",
                "items": [{"name": "Burger", "qty": 1}, {"name": "Fries", "qty": 1}],
                "total": 12.49,
                "status": "Preparing",
                "time": "11:15 AM"
            },
            {
                "id": 1003,
                "customer": "Mitul Uttam",
                "items": [{"name": "Pasta", "qty": 1}, {"name": "Salad", "qty": 1}],
                "total": 18.50,
                "status": "Prepared",
                "time": "11:45 AM"
            },
        ]
        self.display_orders()
        
    def display_orders(self, orders=None):
        """Display orders in the table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        orders_to_display = orders or self.orders
        
        for order in orders_to_display:
            items_text = ", ".join([f"{item['qty']}x {item['name']}" for item in order["items"]])
            self.tree.insert("", "end", values=(
                order["id"],
                order["customer"],
                items_text,
                f"₹{order['total']:.2f}",
                order["status"],
                order["time"]
            ))
            
    def filter_orders(self, event=None):
        """Filter orders by status"""
        status_filter = self.status_filter.get()
        if status_filter == "All":
            self.display_orders()
        else:
            filtered = [order for order in self.orders if order["status"] == status_filter]
            self.display_orders(filtered)
            
    def search_orders(self, event=None):
        """Search orders by customer name or ID"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.display_orders()
            return
            
        filtered = []
        for order in self.orders:
            if (search_term in str(order["id"]).lower() or 
                search_term in order["customer"].lower()):
                filtered.append(order)
                
        self.display_orders(filtered)
        
    def update_selected_orders(self):
        """Update status of selected orders"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more orders")
            return
            
        new_status = self.new_status.get()
        if not new_status:
            return
            
        for item in selected_items:
            order_id = self.tree.item(item)["values"][0]
            for order in self.orders:
                if order["id"] == order_id:
                    order["status"] = new_status
                    break
                    
        self.display_orders()
        messagebox.showinfo("Success", f"Updated {len(selected_items)} order(s) to {new_status}")
        
    def show_order_details(self, event):
        """Show detailed view of selected order"""
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        order_id = self.tree.item(selected_item)["values"][0]
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            return
            
        # Create detail window
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Order Details - #{order_id}")
        detail_win.geometry("500x400")
        
        # Order header
        header = tk.Frame(detail_win, padx=20, pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"Order #{order_id}",
            font=("Helvetica", 16, "bold")
        ).pack(anchor=tk.W)
        
        tk.Label(
            header,
            text=f"Customer: {order['customer']}",
            font=("Helvetica", 12)
        ).pack(anchor=tk.W)
        
        tk.Label(
            header,
            text=f"Status: {order['status']}",
            font=("Helvetica", 12)
        ).pack(anchor=tk.W)
        
        # Items list
        items_frame = tk.Frame(detail_win)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            items_frame,
            text="Items Ordered:",
            font=("Helvetica", 12, "bold")
        ).pack(anchor=tk.W)
        
        for item in order["items"]:
            item_frame = tk.Frame(items_frame)
            item_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                item_frame,
                text=f"{item['qty']} x {item['name']}",
                font=("Helvetica", 11)
            ).pack(side=tk.LEFT)
            
        # Order summary
        summary_frame = tk.Frame(detail_win)
        summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            text=f"Total: ₹{order['total']:.2f}",
            font=("Helvetica", 12, "bold")
        ).pack(side=tk.RIGHT)
        
    def add_new_order(self):
        """Open dialog to add new order"""
        # Implementation for adding new orders would go here
        messagebox.showinfo("Info", "Add new order functionality would be implemented here")
        
    def refresh_orders(self):
        """Refresh orders list"""
        # In a real app, this would fetch from database/API
        self.display_orders()
        messagebox.showinfo("Refreshed", "Order list has been refreshed")
