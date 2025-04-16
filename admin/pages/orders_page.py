import customtkinter as ctk
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
                ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=13), text_color=COLORS["text_primary"]).grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")
                row.grid_columnconfigure(idx, weight=1)
            row.bind("<Double-1>", lambda e, oid=order["id"]: self.show_order_details_by_id(oid))

    def show_order_details_by_id(self, order_id):
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            return
        detail_win = ctk.CTkToplevel(self)
        detail_win.title(f"Order Details - #{order_id}")
        detail_win.geometry("500x400")
        header = ctk.CTkFrame(detail_win, corner_radius=10, fg_color=COLORS["card_bg"], padx=20, pady=10)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text=f"Order #{order_id}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text=f"Special Instructions: {order.get('special_instructions', '')}",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w")
        items_frame = ctk.CTkFrame(detail_win, fg_color=COLORS["bg_main"])
        items_frame.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(
            items_frame,
            text="Items Ordered:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w")
        for item in order["items"]:
            item_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(
                item_frame,
                text=f"{item['qty']} x {item['name']} (Price: {item['price']})",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_primary"]
            ).pack(side="left")
        summary_frame = ctk.CTkFrame(detail_win, fg_color=COLORS["bg_main"])
        summary_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            summary_frame,
            text=f"Total: ₹{order['total']:.2f}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(side="right")
        payment_status = order.get('payment_status', 'unpaid')
        status_label = ctk.CTkLabel(
            summary_frame,
            text=f"Payment Status: {payment_status.capitalize()}",
            font=ctk.CTkFont(size=12),
            text_color="#38B000" if payment_status == "paid" else "#E63946"
        )
        status_label.pack(side="left", padx=10)
        if payment_status != "paid":
            def mark_as_paid():
                try:
                    resp = requests.post(f"http://127.0.0.1:5000/orders/{order_id}/pay", timeout=5)
                    if resp.status_code == 200:
                        ctk.CTkMessagebox.show_info("Success", f"Order #{order_id} marked as paid.")
                        status_label.configure(text="Payment Status: Paid", text_color="#38B000")
                        order['payment_status'] = 'paid'
                        self.apply_filters()
                    else:
                        ctk.CTkMessagebox.show_error("Error", f"Failed to mark as paid: {resp.json().get('message')}")
                except Exception as e:
                    ctk.CTkMessagebox.show_error("Error", f"Request failed: {e}")
            pay_btn = ctk.CTkButton(
                summary_frame,
                text="Mark as Paid",
                fg_color="#38B000",
                hover_color="#2D9300",
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=mark_as_paid,
                corner_radius=8
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
        filter_val = self.filter_var.get()
        filtered = []
        for order in self.orders:
            status = str(order.get("payment_status", "unpaid")).strip().lower()
            status_match = (
                filter_val == "all" or
                (filter_val == "paid" and status == "paid") or
                (filter_val == "unpaid" and status != "paid")
            )
            if status_match:
                filtered.append(order)
        self.display_orders(filtered)
        self.update_idletasks()

    def add_new_order(self):
        ctk.CTkMessagebox.show_info("Info", "Add new order functionality would be implemented here")

    def refresh_orders(self):
        self.load_orders_from_api()
