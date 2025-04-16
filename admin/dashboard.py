import tkinter as tk
from tkinter import ttk
import sys
from utils.colors import COLORS
from utils.widgets import SidebarButton
from pages.items_page import ItemsPage
from pages.add_items_page import AddItemsPage
from pages.revenue_page import RevenuePage
from pages.orders_page import OrdersPage

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        self.parent = parent
        
        # Configure the style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        self.style.configure('TFrame', background=COLORS["bg_main"])
        self.style.configure('TLabel', background=COLORS["bg_main"], foreground=COLORS["text_primary"])
        
        # Create the main layout
        self.create_layout()
        
        # Set default page
        self.show_page("items")
    
    def create_layout(self):
        # Create main container
        self.main_container = tk.Frame(self, bg=COLORS["bg_main"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.sidebar = tk.Frame(self.main_container, bg=COLORS["bg_sidebar"], width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Prevent sidebar from shrinking
        
        # Create content area
        self.content = tk.Frame(self.main_container, bg=COLORS["bg_main"])
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create sidebar header
        self.sidebar_header = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"], height=100)
        self.sidebar_header.pack(fill=tk.X)
        
        # Dashboard title
        self.title_label = tk.Label(
            self.sidebar_header, 
            text="ADMIN DASHBOARD", 
            font=("Helvetica", 16, "bold"),
            bg=COLORS["bg_sidebar"],
            fg=COLORS["text_light"]
        )
        self.title_label.pack(pady=30)
        
        # Sidebar menu
        self.menu_frame = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        self.menu_frame.pack(fill=tk.X, pady=20)
        
        # Create sidebar buttons
        self.items_btn = SidebarButton(self.menu_frame, "Items", lambda: self.show_page("items"))
        self.items_btn.pack(fill=tk.X, pady=5)
        
        self.add_items_btn = SidebarButton(self.menu_frame, "Add Items", lambda: self.show_page("add_items"))
        self.add_items_btn.pack(fill=tk.X, pady=5)
        
        self.revenue_btn = SidebarButton(self.menu_frame, "Revenue", lambda: self.show_page("revenue"))
        self.revenue_btn.pack(fill=tk.X, pady=5)
        
        self.orders_btn = SidebarButton(self.menu_frame, "Orders", lambda: self.show_page("orders"))
        self.orders_btn.pack(fill=tk.X, pady=5)
        
        # Create footer with logout button
        self.sidebar_footer = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        self.sidebar_footer.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        self.logout_btn = SidebarButton(
            self.sidebar_footer, 
            "Logout", 
            self.logout,
            bg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"]
        )
        self.logout_btn.pack(fill=tk.X, pady=5, padx=20)
        
        # Initialize pages dictionary
        self.pages = {}
        
    def show_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()
        
        # Create page if it doesn't exist
        if page_name not in self.pages:
            if page_name == "items":
                self.pages[page_name] = ItemsPage(self.content)
            elif page_name == "add_items":
                self.pages[page_name] = AddItemsPage(self.content)
            elif page_name == "revenue":
                self.pages[page_name] = RevenuePage(self.content)
            elif page_name == "orders":
                self.pages[page_name] = OrdersPage(self.content)
        
        # Show selected page
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        
        # Update active button
        self.items_btn.set_active(page_name == "items")
        self.add_items_btn.set_active(page_name == "add_items")
        self.revenue_btn.set_active(page_name == "revenue")
        self.orders_btn.set_active(page_name == "orders")
    
    def logout(self):
        if tk.messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            sys.exit()

