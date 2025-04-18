import customtkinter as ctk
import tkinter as tk
import requests
import json
from utils.colors import COLORS
from utils.widgets import Card

class OrdersPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg_main"])
        self.parent = parent
        self.orders = []
        self.setup_header()
        self.setup_content()
        self.setup_footer()
        self.load_sample_orders()

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
        self.create_orders_table()

    def create_orders_table(self):
        columns = ("Order ID", "Items", "Special Instructions", "Total")
        self.table_frame = ctk.CTkFrame(self.content, fg_color=COLORS["bg_main"])
        self.table_frame.pack(fill="both", expand=True)
        header_row = ctk.CTkFrame(self.table_frame, fg_color=COLORS["card_bg"], corner_radius=10)
        header_row.pack(fill="x", pady=(0, 2))
        for idx, col in enumerate(columns):
            ctk.CTkLabel(header_row, text=col, font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["primary"]).grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")
            header_row.grid_columnconfigure(idx, weight=1)
        self.rows_container = ctk.CTkFrame(self.table_frame, fg_color=COLORS["bg_main"])
        self.rows_container.pack(fill="both", expand=True)
        self.display_orders()

    def display_orders(self, orders=None):
        for widget in self.rows_container.winfo_children():
            widget.destroy()
        orders_to_display = orders or self.orders
        for order in orders_to_display:
            row = ctk.CTkFrame(self.rows_container, fg_color=COLORS["card_bg"], corner_radius=8)
            row.pack(fill="x", pady=2, padx=0)
            items_text = ", ".join([f"{item['qty']}x {item['name']}" for item in order["items"]])
            values = [order["id"], items_text, order.get("special_instructions", ""), f"₹{order['total']:.2f}"]
            for idx, val in enumerate(values):
                label = ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=13), text_color=COLORS["text_primary"])
                label.grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")
                row.grid_columnconfigure(idx, weight=1)
                # Make label clickable as well
                label.bind("<Button-1>", lambda e, oid=order["id"]: self.show_order_details_by_id(oid))
            # Make the whole row clickable on single click
            row.bind("<Button-1>", lambda e, oid=order["id"]: self.show_order_details_by_id(oid))

    def show_order_details_by_id(self, order_id):
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            return
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Order Details - #{order_id}")
        detail_win.geometry("500x400")
        detail_win.configure(bg=COLORS["bg_main"])
        # Header
        header = tk.Frame(detail_win, bg=COLORS["card_bg"])
        header.pack(fill="x", padx=20, pady=10)
        tk.Label(
            header,
            text=f"Order #{order_id}",
            font=("Arial", 16, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["card_bg"]
        ).pack(anchor="w")
        tk.Label(
            header,
            text=f"Special Instructions: {order.get('special_instructions', '')}",
            font=("Arial", 12),
            fg=COLORS["text_secondary"],
            bg=COLORS["card_bg"]
        ).pack(anchor="w")
        # Items
        items_frame = tk.Frame(detail_win, bg=COLORS["bg_main"])
        items_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(
            items_frame,
            text="Items Ordered:",
            font=("Arial", 12, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["bg_main"]
        ).pack(anchor="w")
        for item in order["items"]:
            item_frame = tk.Frame(items_frame, bg=COLORS["bg_main"])
            item_frame.pack(fill="x", pady=2)
            tk.Label(
                item_frame,
                text=f"{item['qty']} x {item['name']} (Price: {item['price']})",
                font=("Arial", 11),
                fg=COLORS["text_primary"],
                bg=COLORS["bg_main"]
            ).pack(side="left")
        # Summary
        summary_frame = tk.Frame(detail_win, bg=COLORS["card_bg"])
        summary_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(
            summary_frame,
            text=f"Total: ₹{order['total']:.2f}",
            font=("Arial", 12, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["card_bg"]
        ).pack(side="right")
        payment_status = order.get('payment_status', 'unpaid')
        status_label = tk.Label(
            summary_frame,
            text=f"Payment Status: {payment_status.capitalize()}",
            font=("Arial", 12),
            fg="#38B000" if payment_status == "paid" else "#E63946",
            bg=COLORS["card_bg"]
        )
        status_label.pack(side="left", padx=10)
        if payment_status != "paid":
            def mark_as_paid():
                try:
                    resp = requests.post(f"http://127.0.0.1:5000/orders/{order_id}/pay", timeout=5)
                    if resp.status_code == 200:
                        status_label.config(text="Payment Status: Paid", fg="#38B000")
                        order['payment_status'] = 'paid'
                        self.apply_filters()
                        tk.messagebox.showinfo("Success", f"Order #{order_id} marked as paid.")
                    else:
                        tk.messagebox.showerror("Error", f"Failed to mark as paid: {resp.json().get('message')}")
                except Exception as e:
                    tk.messagebox.showerror("Error", f"Request failed: {e}")
            pay_btn = tk.Button(
                summary_frame,
                text="Mark as Paid",
                bg="#38B000",
                fg="white",
                font=("Arial", 12, "bold"),
                command=mark_as_paid,
                relief=tk.RAISED,
                activebackground="#2D9300"
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
                orders = data.get('orders', [])
                self.orders = orders
                self.apply_filters()
            else:
                ctk.CTkMessagebox.show_error("Error", f"Failed to fetch orders: {resp.status_code}")
        except Exception as e:
            ctk.CTkMessagebox.show_error("Error", f"Request failed: {e}")

    def load_sample_orders(self):
        self.load_orders_from_api()

    def apply_filters(self):
        filter_val = self.filter_var.get().strip().lower()
        filtered = []
        for order in self.orders:
            # Normalize payment_status for robust comparison
            status = str(order.get("payment_status", "unpaid")).strip().lower()
            if filter_val == "all":
                filtered.append(order)
            elif filter_val == "paid" and status == "paid":
                filtered.append(order)
            elif filter_val == "unpaid" and status != "paid":
                filtered.append(order)
        self.display_orders(filtered)
        self.update_idletasks()

    def add_new_order(self):
        ctk.CTkMessagebox.show_info("Info", "Add new order functionality would be implemented here")

    def refresh_orders(self):
        self.load_orders_from_api()