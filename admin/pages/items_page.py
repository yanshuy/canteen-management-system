import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import os
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
            bg=COLORS["bg_card"],
            padx=15,
            pady=15,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0,
            relief=tk.RAISED
        )
        
        self.item_data = item_data
        
        # Create grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        # Image container with rounded corners
        self.image_container = tk.Frame(self, bg=COLORS["border"])
        self.image_container.grid(row=0, column=0, rowspan=4, padx=(0, 15), sticky="nsew")
        self.image_container.grid_propagate(False)
        self.image_container.configure(width=150, height=150)
        
        # Load image from assets
        self.load_image()
        
        # Item name
        self.name_label = tk.Label(
            self,
            text=item_data["name"],
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w",
            justify="left"
        )
        self.name_label.grid(row=0, column=1, sticky="w")
        
        # Item category with modern pill design
        self.category_pill = tk.Frame(self, bg="#E0F2FE", bd=0)
        self.category_pill.grid(row=1, column=1, sticky="w", pady=(0, 5))
        
        self.category_label = tk.Label(
            self.category_pill,
            text=item_data["category"],
            font=("Segoe UI", 9),
            bg="#E0F2FE",
            fg="#0369A1",
            padx=8,
            pady=2
        )
        self.category_label.pack()
        
        # Item price
        self.price_frame = tk.Frame(self, bg=COLORS["bg_card"])
        self.price_frame.grid(row=2, column=1, sticky="w", pady=(0, 10))
        
        self.price_label = tk.Label(
            self.price_frame,
            text=f"₹{item_data['price']:.2f}",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        )
        self.price_label.pack(side=tk.LEFT)
        
        if item_data.get("old_price"):
            self.old_price_label = tk.Label(
                self.price_frame,
                text=f"₹{item_data['old_price']:.2f}",
                font=("Segoe UI", 10),
                bg=COLORS["bg_card"],
                fg=COLORS["text_secondary"],
                padx=5
            )
            self.old_price_label.pack(side=tk.LEFT)
            
            # Add strikethrough to old price
            self.old_price_label.update()
            x, y = 0, self.old_price_label.winfo_height() // 2
            width = self.old_price_label.winfo_width()
            self.canvas = tk.Canvas(
                self.old_price_label, 
                width=width, 
                height=1, 
                bg=COLORS["text_secondary"],
                highlightthickness=0
            )
            self.canvas.place(x=x, y=y)
        
        # Action buttons with modern style
        self.button_frame = tk.Frame(self, bg=COLORS["bg_card"])
        self.button_frame.grid(row=3, column=1, sticky="w")
        
        self.edit_button = tk.Button(
            self.button_frame,
            text="Edit",
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 10),
            padx=12,
            pady=4,
            bd=0,
            cursor="hand2",
            activebackground=COLORS["primary_hover"],
            activeforeground=COLORS["text_light"],
            relief=tk.FLAT
        )
        self.edit_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_button = tk.Button(
            self.button_frame,
            text="Delete",
            bg=COLORS["danger"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 10),
            padx=12,
            pady=4,
            bd=0,
            cursor="hand2",
            activebackground=COLORS["danger_hover"],
            activeforeground=COLORS["text_light"],
            relief=tk.FLAT
        )
        self.delete_button.pack(side=tk.LEFT)
        
        # Stock status with modern pill design
        stock_bg = "#DCFCE7" if item_data["in_stock"] else "#FEE2E2"
        stock_fg = "#166534" if item_data["in_stock"] else "#991B1B"
        stock_text = "In Stock" if item_data["in_stock"] else "Out of Stock"
        
        self.stock_pill = tk.Frame(self, bg=stock_bg, bd=0)
        self.stock_pill.grid(row=0, column=1, sticky="e")
        
        self.stock_label = tk.Label(
            self.stock_pill,
            text=stock_text,
            font=("Segoe UI", 9),
            bg=stock_bg,
            fg=stock_fg,
            padx=8,
            pady=2
        )
        self.stock_label.pack()
    
    def load_image(self):
        try:
            # Get the absolute path to the assets folder
            assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            
            # Try to find the image in assets (assuming item_data has an image_name field)
            image_name = self.item_data.get("image_name", "default.png")
            image_path = os.path.join(assets_path, image_name)
            
            # If the specified image doesn't exist, try to use one of the existing assets
            if not os.path.exists(image_path):
                # List all files in the assets directory
                available_images = [f for f in os.listdir(assets_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
                
                if available_images:
                    # Use any image from the assets directory
                    image_path = os.path.join(assets_path, available_images[0])
                else:
                    # Use dynamically created default image if no images exist
                    img = create_default_image()
                    return
            
            # Open and resize the image
            img = Image.open(image_path)
            img = img.resize((120, 120), Image.LANCZOS)
            
            # Convert to RGBA if it's not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create rounded corners mask
            mask = Image.new("L", (120, 120), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle((0, 0, 120, 120), radius=10, fill=255)
            
            # Create a blank RGBA image
            rounded_img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
            # Paste the original image using the mask as alpha
            rounded_img.paste(img, (0, 0), mask)
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(rounded_img)
            
            # Create label inside the container
            self.image_label = tk.Label(
                self.image_container,
                image=photo,
                bg=COLORS["border"],
                bd=0
            )
            self.image_label.image = photo  # Keep a reference
            self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            # Fallback to text if image loading fails
            self.image_label = tk.Label(
                self.image_container,
                text="No Image",
                font=("Segoe UI", 10),
                bg=COLORS["border"],
                fg=COLORS["text_secondary"]
            )
            self.image_label.pack(fill=tk.BOTH, expand=True)

class ItemsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # Sample data with references to local image files
        self.items_data = [
            {
                "id": 1,
                "name": "Medu Vada with Inji Chutney",
                "category": "South Indian",
                "price": 120.00,
                "old_price": 150.00,
                "in_stock": True,
                "image_name": "medu_vada.png"
            },
            {
                "id": 2,
                "name": "Masala Dosa",
                "category": "South Indian",
                "price": 150.00,
                "in_stock": True,
                "image_name": "masala_dosa.png"
            },
            {
                "id": 3,
                "name": "Paneer Butter Masala",
                "category": "North Indian",
                "price": 220.00,
                "old_price": 250.00,
                "in_stock": True,
                "image_name": "paneer_butter.png"
            },
            {
                "id": 4,
                "name": "Vegetable Biryani",
                "category": "Main Course",
                "price": 180.00,
                "in_stock": False,
                "image_name": "biryani.png"
            },
            {
                "id": 5,
                "name": "Sandwich",
                "category": "Dessert",
                "price": 80.00,
                "in_stock": True,
                "image_name": "gulab_jamun.png"
            }
        ]
        
        # Page header with modern design
        self.header = tk.Frame(self, bg=COLORS["bg_main"], height=80)
        self.header.pack(fill=tk.X, padx=20, pady=10)
        
        self.title = tk.Label(
            self.header,
            text="Menu Items",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"]
        )
        self.title.pack(side=tk.LEFT)
        
       
        
        # Search and filter section with modern design
        self.search_frame = tk.Frame(self.header, bg=COLORS["bg_main"])
        self.search_frame.pack(side=tk.RIGHT, padx=20)
        
        # Modern search entry
        self.search_entry = tk.Entry(
            self.search_frame,
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            insertbackground=COLORS["text_primary"],
            width=25
        )
        self.search_entry.insert(0, "Search items...")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        # Modern search button
        self.search_button = tk.Button(
            self.search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
            padx=10,
            pady=2,
            bd=0,
            cursor="hand2",
            activebackground=COLORS["primary_hover"],
            activeforeground=COLORS["text_light"],
            relief=tk.FLAT
        )
        self.search_button.pack(side=tk.LEFT)
        
        # Stats cards with modern design
        self.stats_frame = tk.Frame(self, bg=COLORS["bg_main"])
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Total items card
        self.total_items_card = Card(self.stats_frame, width=200, height=100)
        self.total_items_card.pack(side=tk.LEFT, padx=(0, 10))
        
        self.total_items_label = tk.Label(
            self.total_items_card,
            text="TOTAL ITEMS",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.total_items_label.pack(anchor="w", pady=(10, 0))
        
        self.total_items_value = tk.Label(
            self.total_items_card,
            text=str(len(self.items_data)),
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        )
        self.total_items_value.pack(anchor="w", pady=5)
        
        # In stock card
        self.in_stock_card = Card(self.stats_frame, width=200, height=100)
        self.in_stock_card.pack(side=tk.LEFT, padx=(0, 10))
        
        self.in_stock_label = tk.Label(
            self.in_stock_card,
            text="IN STOCK",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.in_stock_label.pack(anchor="w", pady=(10, 0))
        
        in_stock_count = sum(1 for item in self.items_data if item["in_stock"])
        self.in_stock_value = tk.Label(
            self.in_stock_card,
            text=str(in_stock_count),
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["secondary"]
        )
        self.in_stock_value.pack(anchor="w", pady=5)
        
        # Out of stock card
        self.out_stock_card = Card(self.stats_frame, width=200, height=100)
        self.out_stock_card.pack(side=tk.LEFT)
        
        self.out_stock_label = tk.Label(
            self.out_stock_card,
            text="OUT OF STOCK",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.out_stock_label.pack(anchor="w", pady=(10, 0))
        
        out_stock_count = sum(1 for item in self.items_data if not item["in_stock"])
        self.out_stock_value = tk.Label(
            self.out_stock_card,
            text=str(out_stock_count),
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["danger"]
        )
        self.out_stock_value.pack(anchor="w", pady=5)
        
        # Content area with smooth scrolling
        self.content_frame = tk.Frame(self, bg=COLORS["bg_main"])
        # Adjust padding and alignment for better alignment
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        self.scroll_canvas = SmoothScroll(self.content_frame)
        self.scroll_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.scroll_canvas.scrollbar.pack(side="right", fill="y", padx=(0, 10))

        # Add item cards with consistent spacing and alignment
        for idx, item in enumerate(self.items_data):
            card = ItemCard(self.scroll_canvas.scrollable_frame, item)
            card.pack(fill=tk.X, pady=10, padx=10)  # Adjusted padding for alignment

            # Add subtle separator between cards (except last one)
            if idx < len(self.items_data) - 1:
                separator = tk.Frame(
                    self.scroll_canvas.scrollable_frame,
                    height=1,
                    bg=COLORS["border"]
                )
                separator.pack(fill=tk.X, pady=(5, 10))  # Adjusted padding for alignment