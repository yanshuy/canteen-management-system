import customtkinter as ctk
import tkinter as tk
# Add messagebox import
from tkinter import messagebox
import requests
import json
from utils.colors import COLORS
from utils.widgets import Card

class OrdersPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg_main"])
        self.parent = parent
        self.orders = [] # Initialize with an empty list
        self.setup_header()
        self.setup_content()
        self.setup_footer()
        # Load orders after UI is set up
        self.load_orders_from_api() # Changed from load_sample_orders

    def setup_header(self):
        self.header = ctk.CTkFrame(self, fg_color=COLORS["bg_main"], height=70)
        self.header.pack(fill="x")
        self.title = ctk.CTkLabel(
            self.header,
            text="Order Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.title.pack(side="left", padx=20, pady=20)
        filter_frame = ctk.CTkFrame(self.header, fg_color=COLORS["bg_main"])
        filter_frame.pack(side="right", padx=20)
        self.filter_var = ctk.StringVar(value="all")
        filter_all = ctk.CTkRadioButton(
            filter_frame, text="All", variable=self.filter_var, value="all", command=self.apply_filters,
            fg_color=COLORS["primary"], border_color=COLORS["primary"], text_color=COLORS["primary"]
        )
        filter_paid = ctk.CTkRadioButton(
            filter_frame, text="Paid", variable=self.filter_var, value="paid", command=self.apply_filters,
            fg_color=COLORS["secondary"], border_color=COLORS["secondary"], text_color=COLORS["secondary"]
        )
        filter_unpaid = ctk.CTkRadioButton(
            filter_frame, text="Unpaid", variable=self.filter_var, value="unpaid", command=self.apply_filters,
            fg_color=COLORS["danger"], border_color=COLORS["danger"], text_color=COLORS["danger"]
        )
        filter_all.pack(side="left", padx=6)
        filter_paid.pack(side="left", padx=6)
        filter_unpaid.pack(side="left", padx=6)

    def setup_content(self):
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        self.content.pack(fill="both", expand=True, padx=20, pady=10)
        # Ensure content frame resizes properly
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.create_orders_table()

    def create_orders_table(self):
        columns = ("Order ID", "Items", "Special Instructions", "Total")
        # Make table_frame expand within content using grid
        self.table_frame = ctk.CTkFrame(self.content, fg_color=COLORS["bg_main"])
        self.table_frame.grid(row=0, column=0, sticky="nsew") # Use grid instead of pack
        self.table_frame.grid_rowconfigure(1, weight=1) # Allow rows_container to expand vertically
        self.table_frame.grid_columnconfigure(0, weight=1) # Allow header/rows_container to expand horizontally

        header_row = ctk.CTkFrame(self.table_frame, fg_color=COLORS["card_bg"], corner_radius=10)
        # Use grid for header_row as well
        header_row.grid(row=0, column=0, sticky="ew", pady=(0, 2))
        for idx, col in enumerate(columns):
            ctk.CTkLabel(header_row, text=col, font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["primary"]).grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")
            header_row.grid_columnconfigure(idx, weight=1) # Configure columns within header

        # Make rows_container expand within table_frame using grid
        self.rows_container = ctk.CTkFrame(self.table_frame, fg_color=COLORS["bg_main"])
        self.rows_container.grid(row=1, column=0, sticky="nsew") # Use grid
        self.rows_container.grid_columnconfigure(0, weight=1) # Allow rows to expand horizontally

        # Don't call display_orders here, it will be called after loading data

    def display_orders(self, orders_to_display=None):
        # Clear existing widgets more reliably
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        # Use the provided list or the instance's list
        if orders_to_display is None:
            orders_to_display = self.orders

        if not orders_to_display:
            no_orders_label = ctk.CTkLabel(self.rows_container, text="No orders found.", font=ctk.CTkFont(size=15, weight="bold"), text_color=COLORS["danger"])
            # Use grid for the label too
            no_orders_label.grid(row=0, column=0, pady=20, sticky="ew")
            # Ensure the container knows about this single row
            self.rows_container.grid_rowconfigure(0, weight=0) # Don't let empty message expand
        else:
            for i, order in enumerate(orders_to_display): # Use enumerate for row index
                row = ctk.CTkFrame(self.rows_container, fg_color=COLORS["card_bg"], corner_radius=8)
                # Use grid for rows, ensure they fill horizontally
                row.grid(row=i, column=0, sticky="ew", pady=2, padx=0)
                # Configure columns within the row for proper alignment and weighting
                row.grid_columnconfigure(0, weight=1) # Order ID
                row.grid_columnconfigure(1, weight=3) # Items (more space)
                row.grid_columnconfigure(2, weight=2) # Special Instructions
                row.grid_columnconfigure(3, weight=1) # Total

                items_text = ", ".join([f"{item['qty']}x {item['name']}" for item in order["items"]])
                values = [order["id"], items_text, order.get("special_instructions", ""), f"₹{order['total']:.2f}"]

                for idx, val in enumerate(values):
                    # Make labels wrap text if needed, especially for items/instructions
                    # Estimate wrap length based on column weight (adjust as needed)
                    wrap_len = 0
                    if idx == 1: wrap_len = 300 # Items column
                    elif idx == 2: wrap_len = 200 # Instructions column

                    label = ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=13), text_color=COLORS["text_primary"], anchor="w", justify="left", wraplength=wrap_len)
                    # Adjust sticky based on column if needed, 'w' or 'ew' often good
                    label.grid(row=0, column=idx, padx=8, pady=8, sticky="ew") # Use ew for horizontal fill
                    label.bind("<Button-1>", lambda e, oid=order["id"]: self.show_order_details_by_id(oid))

                row.bind("<Button-1>", lambda e, oid=order["id"]: self.show_order_details_by_id(oid))
                # Configure the row index in the container
                self.rows_container.grid_rowconfigure(i, weight=0) # Give rows minimal vertical space

        # Force update after modifications
        self.rows_container.update_idletasks()
        # Also update the parent content frame if necessary
        self.content.update_idletasks()

    def show_order_details_by_id(self, order_id):
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            return
        # Use standard tkinter messagebox and widgets for the popup
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Order Details - #{order_id}")
        detail_win.geometry("500x400")
        detail_win.configure(bg=COLORS["bg_main"]) # Use a standard color name or hex

        # Header Frame (using tk)
        header = tk.Frame(detail_win, bg=COLORS["card_bg"]) # Use a standard color name or hex
        header.pack(fill="x", padx=20, pady=10)
        tk.Label(
            header,
            text=f"Order #{order_id}",
            font=("Arial", 16, "bold"),
            fg=COLORS["primary"], # Use a standard color name or hex
            bg=COLORS["card_bg"] # Use a standard color name or hex
        ).pack(anchor="w")
        tk.Label(
            header,
            text=f"Special Instructions: {order.get('special_instructions', 'None')}", # Provide default
            font=("Arial", 12),
            fg=COLORS["text_secondary"], # Use a standard color name or hex
            bg=COLORS["card_bg"], # Use a standard color name or hex
            wraplength=450, # Allow wrapping for long instructions
            justify="left"
        ).pack(anchor="w")

        # Items Frame (using tk)
        items_frame = tk.Frame(detail_win, bg=COLORS["bg_main"]) # Use a standard color name or hex
        items_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(
            items_frame,
            text="Items Ordered:",
            font=("Arial", 12, "bold"),
            fg=COLORS["primary"], # Use a standard color name or hex
            bg=COLORS["bg_main"] # Use a standard color name or hex
        ).pack(anchor="w")
        # Scrollable area for items if there are many
        items_canvas = tk.Canvas(items_frame, bg=COLORS["bg_main"], highlightthickness=0)
        items_scrollbar = tk.Scrollbar(items_frame, orient="vertical", command=items_canvas.yview)
        scrollable_items_frame = tk.Frame(items_canvas, bg=COLORS["bg_main"])

        scrollable_items_frame.bind(
            "<Configure>",
            lambda e: items_canvas.configure(
                scrollregion=items_canvas.bbox("all")
            )
        )

        items_canvas.create_window((0, 0), window=scrollable_items_frame, anchor="nw")
        items_canvas.configure(yscrollcommand=items_scrollbar.set)

        items_canvas.pack(side="left", fill="both", expand=True)
        items_scrollbar.pack(side="right", fill="y")


        for item in order["items"]:
            item_text = f"{item['qty']} x {item['name']} (Price: ₹{item['price']:.2f})"
            tk.Label(
                scrollable_items_frame, # Add labels to the scrollable frame
                text=item_text,
                font=("Arial", 11),
                fg=COLORS["text_primary"], # Use a standard color name or hex
                bg=COLORS["bg_main"], # Use a standard color name or hex
                anchor="w",
                justify="left"
            ).pack(fill="x", pady=1) # Fill horizontally

        # Summary Frame (using tk)
        summary_frame = tk.Frame(detail_win, bg=COLORS["card_bg"]) # Use a standard color name or hex
        summary_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(
            summary_frame,
            text=f"Total: ₹{order['total']:.2f}",
            font=("Arial", 12, "bold"),
            fg=COLORS["primary"], # Use a standard color name or hex
            bg=COLORS["card_bg"] # Use a standard color name or hex
        ).pack(side="right", padx=10) # Add padding

        payment_status = str(order.get('payment_status', 'unpaid')).strip().lower() # Normalize here too
        status_label = tk.Label(
            summary_frame,
            text=f"Payment Status: {payment_status.capitalize()}",
            font=("Arial", 12),
            fg="#38B000" if payment_status == "paid" else "#E63946", # Use standard hex colors
            bg=COLORS["card_bg"] # Use a standard color name or hex
        )
        status_label.pack(side="left", padx=10)

        if payment_status != "paid":
            def mark_as_paid():
                try:
                    resp = requests.post(f"http://127.0.0.1:5000/orders/{order_id}/pay", timeout=5)
                    if resp.status_code == 200:
                        status_label.config(text="Payment Status: Paid", fg="#38B000")
                        # Find and update the order in the main list
                        for o in self.orders:
                            if o["id"] == order_id:
                                o['payment_status'] = 'paid'
                                break
                        # Refresh the main view based on current filter
                        self.apply_filters()
                        messagebox.showinfo("Success", f"Order #{order_id} marked as paid.")
                        # Optionally close the detail window after success
                        # detail_win.destroy()
                    else:
                        messagebox.showerror("Error", f"Failed to mark as paid: {resp.json().get('message')}")
                except Exception as e:
                    messagebox.showerror("Error", f"Request failed: {e}")
            pay_btn = tk.Button(
                summary_frame,
                text="Mark as Paid",
                bg="#38B000", # Use standard hex colors
                fg="white",
                font=("Arial", 12, "bold"),
                command=mark_as_paid,
                relief=tk.RAISED,
                activebackground="#2D9300" # Use standard hex colors
            )
            pay_btn.pack(side="left", padx=10)

    def setup_footer(self):
        footer = ctk.CTkFrame(self, fg_color=COLORS["bg_main"], height=60)
        footer.pack(fill="x", padx=20, pady=10)
        action_frame = ctk.CTkFrame(footer, fg_color=COLORS["bg_main"])
        action_frame.pack(side="right")
        refresh_btn = ctk.CTkButton(
            action_frame,
            text="Refresh",
            command=self.refresh_orders,
            fg_color=COLORS["secondary"],
            hover_color=COLORS["primary"],
            text_color="white",
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10,
            width=120,
            height=40
        )
        refresh_btn.pack(side="left", padx=8)

    def load_orders_from_api(self):
        try:
            resp = requests.get("http://127.0.0.1:5000/orders", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                orders_data = data.get('orders', [])
                # Normalize payment_status during loading
                for order in orders_data:
                    order['payment_status'] = str(order.get('payment_status', 'unpaid')).strip().lower()
                    if order['payment_status'] not in ('paid', 'unpaid'):
                         order['payment_status'] = 'unpaid' # Default invalid status
                self.orders = orders_data
                self.apply_filters() # Apply filters which calls display_orders
            else:
                # Use standard tkinter messagebox
                messagebox.showerror("Error", f"Failed to fetch orders: {resp.status_code}")
                self.orders = [] # Clear orders on failure
                self.display_orders() # Display empty state
        except Exception as e:
            messagebox.showerror("Error", f"Request failed: {e}")
            self.orders = [] # Clear orders on exception
            self.display_orders() # Display empty state

    def load_sample_orders(self):
        # This method might be deprecated if API is always used
        # If kept, ensure it normalizes status like load_orders_from_api
        print("Loading sample orders (consider removing if API is primary)")
        # Example sample data structure (ensure status is lowercase)
        self.orders = [
             {'id': 'SAMPLE001', 'items': [{'name': 'Test Item', 'qty': 1, 'price': 10.0}], 'special_instructions': 'None', 'total': 10.0, 'payment_status': 'unpaid'},
             {'id': 'SAMPLE002', 'items': [{'name': 'Another Item', 'qty': 2, 'price': 5.0}], 'special_instructions': 'Extra sauce', 'total': 10.0, 'payment_status': 'paid'}
        ]
        self.apply_filters()

    def apply_filters(self):
        filter_val = self.filter_var.get()
        filtered = []
        for order in self.orders:
            # Status is already normalized during load
            status = order.get("payment_status", "unpaid") # Default just in case
            status_match = (
                filter_val == "all" or
                (filter_val == "paid" and status == "paid") or
                (filter_val == "unpaid" and status == "unpaid")
            )
            if status_match:
                filtered.append(order)
        print(f"Filtering by '{filter_val}', found {len(filtered)} orders.") # Debug print
        self.display_orders(filtered) # Pass the filtered list
        # No need for self.update_idletasks() here, display_orders handles it

    def add_new_order(self):
        # Use standard tkinter messagebox
        messagebox.showinfo("Info", "Add new order functionality would be implemented here")

    def refresh_orders(self):
        print("Refreshing orders...") # Debug print
        self.load_orders_from_api()
