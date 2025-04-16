import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import os
import requests
from utils.colors import COLORS
from utils.widgets import Card
from utils.images import create_default_image

class SmoothScroll(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.config(bg=COLORS["bg_main"], highlightthickness=0)
        
        # Create scrollable frame
        self.scrollable_frame = tk.Frame(self, bg=COLORS["bg_main"])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.configure(scrollregion=self.bbox("all"))
        )
        
        self.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure smooth scrolling
        self.bind("<Configure>", self._on_configure)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)
        
        # Style the scrollbar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", 
                       background=COLORS["border"],
                       troughcolor=COLORS["bg_main"],
                       bordercolor=COLORS["border"],
                       arrowcolor=COLORS["text_primary"],
                       lightcolor=COLORS["border"],
                       darkcolor=COLORS["border"])
        
    def _on_configure(self, event):
        self.configure(scrollregion=self.bbox("all"))
        
    def _on_mousewheel(self, event):
        self.yview_scroll(int(-1*(event.delta/120)), "units")

class ItemCard(tk.Frame):
    def __init__(self, parent, item_data):
        super().__init__(
            parent,
            bg="#F8FAFC",  # Light card background
            padx=15,
            pady=15,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0,
            relief=tk.RAISED
        )
        self.item_data = item_data
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        # Image
        self.image_container = tk.Frame(self, bg="#E0E7EF", width=110, height=110)
        self.image_container.grid(row=0, column=0, rowspan=3, padx=(0, 18), sticky="n")
        self.image_container.grid_propagate(False)
        self._load_image()
        # Name
        self.name_label = tk.Label(
            self,
            text=item_data["name"],
            font=("Segoe UI", 15, "bold"),
            bg="#F8FAFC",
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.name_label.grid(row=0, column=1, sticky="w")
        # Categories as colored pills
        cat_frame = tk.Frame(self, bg="#F8FAFC")
        cat_frame.grid(row=1, column=1, sticky="w", pady=(2, 0))
        for cat in item_data["category"]:
            pill = tk.Label(
                cat_frame,
                text=cat,
                font=("Segoe UI", 9, "bold"),
                bg="#E0F2FE",
                fg="#0369A1",
                padx=8,
                pady=2,
                bd=0,
                relief=tk.FLAT
            )
            pill.pack(side=tk.LEFT, padx=(0, 6))
        # Price
        self.price_label = tk.Label(
            self,
            text=f"₹{item_data['price']:.2f}",
            font=("Segoe UI", 13, "bold"),
            bg="#F8FAFC",
            fg=COLORS["accent"]
        )
        self.price_label.grid(row=2, column=1, sticky="w", pady=(8, 0))
       
    def _load_image(self):
        try:
            assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            image_name = self.item_data.get("image_name", "default.png")
            image_path = os.path.join(assets_path, image_name)
            if not os.path.exists(image_path):
                available_images = [f for f in os.listdir(assets_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
                if available_images:
                    image_path = os.path.join(assets_path, available_images[0])
                else:
                    img = create_default_image()
                    return
            img = Image.open(image_path)
            img = img.resize((100, 100), Image.LANCZOS)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            mask = Image.new("L", (100, 100), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle((0, 0, 100, 100), radius=12, fill=255)
            rounded_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
            rounded_img.paste(img, (0, 0), mask)
            photo = ImageTk.PhotoImage(rounded_img)
            self.image_label = tk.Label(
                self.image_container,
                image=photo,
                bg="#E0E7EF",
                bd=0
            )
            self.image_label.image = photo
            self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        except Exception as e:
            self.image_label = tk.Label(
                self.image_container,
                text="No Image",
                font=("Segoe UI", 10),
                bg="#E0E7EF",
                fg=COLORS["text_secondary"]
            )
            self.image_label.pack(fill=tk.BOTH, expand=True)

class ItemsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg_main"])
        self.items_data = []
        self.filtered_items = []
        self.categories = ["All"]
        self.selected_category = ctk.StringVar(value="All")

        # Page header with modern design
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.header.pack(fill="x", padx=55, pady=10)

        self.title = ctk.CTkLabel(
            self.header,
            text="Menu Items",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.title.pack(side="left")

        # Filter dropdown
        self.filter_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.filter_frame.pack(side="left", padx=(20, 0))
        self.category_menu = ctk.CTkComboBox(
            self.filter_frame,
            variable=self.selected_category,
            values=self.categories,
            font=ctk.CTkFont(size=12),
            width=140,
            command=lambda _: self.apply_filters(),
            fg_color="white",  # Make input white
            border_width=2,
            border_color=COLORS["border"],
            corner_radius=10,  # More rounding
            dropdown_fg_color="white",  # White dropdown background
            dropdown_text_color=COLORS["text_primary"],  # Theme text color
            button_color=COLORS["primary"],  # Blue arrow
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text_primary"]  # Ensure selected text is visible
        )
        self.category_menu.pack(side="left")

        # Search and filter section with modern design
        self.search_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.search_frame.pack(side="right", padx=20)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            font=ctk.CTkFont(size=12),
            width=180,
            placeholder_text="Search items...",
            fg_color="white",  # Make input white
            border_width=2,
            border_color=COLORS["border"],
            corner_radius=10,  # More rounding
            text_color=COLORS["text_primary"],  # Ensure text is visible
            placeholder_text_color=COLORS["text_secondary"]  # Make placeholder visible
        )
        self.search_entry.pack(side="left", padx=(0, 10), ipady=2)
        self.search_entry.bind("<FocusIn>", self._clear_search_placeholder)
        self.search_entry.bind("<Return>", lambda e: self.apply_filters())

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="🔍",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color="white",
            width=40,
            height=32,
            command=self.apply_filters,
            corner_radius=8
        )
        self.search_button.pack(side="left")

        # Refresh button with icon
        self.refresh_button = ctk.CTkButton(
            self.search_frame,
            text="⟳",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS["secondary"],
            hover_color=COLORS["primary"],
            text_color="white",
            width=40,
            height=32,
            command=self.fetch_menu_items,
            corner_radius=8
        )
        self.refresh_button.pack(side="left", padx=(6, 0))

        # Stats cards with modern design
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.total_items_card = Card(self.stats_frame, width=200, height=100)
        self.total_items_card.pack(side="left", padx=(35, 10), pady=(20,0))  # Move inside with more left padding
        self.total_items_label = ctk.CTkLabel(
            self.total_items_card,
            text="TOTAL  ITEMS",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_secondary"]
        )
        self.total_items_label.pack(anchor="w", pady=(10, 0))
        self.total_items_value = ctk.CTkLabel(
            self.total_items_card,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["primary"]
        )
        self.total_items_value.pack(anchor="w", pady=0)

        # Content area with scrollable frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color=COLORS["bg_main"], corner_radius=16)  # More rounding
        self.scroll_frame.pack(fill="both", expand=True, padx=10)

        self.fetch_menu_items()

    def _clear_search_placeholder(self, event):
        if self.search_entry.get() == "Search items...":
            self.search_entry.delete(0, tk.END)

    def fetch_menu_items(self):
        try:
            resp = requests.get("http://127.0.0.1:5000/menu-items", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                # Normalize and convert backend data to expected format
                self.items_data = []
                categories = set()
                for item in items:
                    # Backend may store categories as comma-separated string
                    cats = item.get("category", "").split(",")
                    cats = [c.strip() for c in cats if c.strip()]
                    for c in cats:
                        categories.add(c)
                    self.items_data.append({
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "category": cats if cats else ["Other"],
                        "price": float(item.get("price").replace("₹", "").strip()) if isinstance(item.get("price"), str) else float(item.get("price", 0)),
                        "old_price": None,  # Optionally add old_price if backend supports
                        "image_name": item.get("image_name", "")
                    })
                self.categories = ["All"] + sorted(categories)
                self.category_menu.configure(values=self.categories)
                self.selected_category.set("All")
                self.apply_filters()
            else:
                self.items_data = []
                self.apply_filters()
        except Exception as e:
            print(f"Failed to fetch menu items: {e}")
            self.items_data = []
            self.apply_filters()

    def apply_filters(self):
        search = self.search_entry.get().strip().lower()
        cat = self.selected_category.get()
        filtered = self.items_data
        if cat != "All":
            filtered = [item for item in filtered if cat in item["category"]]
        if search and search != "search items...":
            filtered = [item for item in filtered if search in item["name"].lower()]
        self.filtered_items = filtered
        self.update_stats()
        self.display_items()

    def update_stats(self):
        self.total_items_value.configure(text=str(len(self.filtered_items)))

    def display_items(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for idx, item in enumerate(self.filtered_items):
            card = ItemCard(self.scroll_frame, item)
            card.pack(fill="x", pady=10, padx=10)
            if idx < len(self.filtered_items) - 1:
                separator = ctk.CTkFrame(
                    self.scroll_frame,
                    height=1,
                    fg_color=COLORS["border"]
                )
                separator.pack(fill="x", pady=(5, 10))