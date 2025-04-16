import tkinter
import customtkinter
from PIL import Image, ImageTk
import os
import requests
from io import BytesIO
from services.image_cache import ImageCache

class MenuView:
    def __init__(self, root, menu_service, cart_service, on_view_cart=None):
        self.root = root
        self.menu_service = menu_service
        self.cart_service = cart_service
        self.on_view_cart = on_view_cart  # Callback for when Cart is clicked
        
        # Create placeholder image
        self.placeholder_image = customtkinter.CTkImage(
            Image.new("RGB", (100, 100), "gray"), 
            size=(100, 100)
        )
        
        # Initialize the image cache
        self.image_cache = ImageCache()
        
        # Keep track of image labels for updating
        self.image_labels = {}
        
        # Define color scheme
        self.colors = {
            "primary": "#4D77FF",
            "secondary": "#5C77E6",
            "accent": "#FF8C32",
            "success": "#38B000",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "card_bg": ("#FFFFFF", "#2B2B2B"),
            "hover": ("#E6E6E6", "#3A3A3A"),
            "border": ("#E0E0E0", "#3A3A3A") 
        }
        
        self._create_ui()
        
    def _create_ui(self):
        # UI Elements
        self._create_header()
        self._create_filter_buttons()
        self._create_scrollable_frame()
        
        # Display all items initially
        self.filter_items("All")
        
    def _create_header(self):
        header_frame = customtkinter.CTkFrame(self.root, fg_color="transparent", corner_radius=0)
        header_frame.pack(pady=(20, 15), fill="x", padx=25)  
        
        title_frame = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", anchor="w")
        
        title = customtkinter.CTkLabel(
            title_frame, 
            text="🍴 Canteeny",  
            font=customtkinter.CTkFont(size=24, weight="bold"),
            compound="left" 
        )
        title.pack(side="left", pady=0, padx=0)
            
        # Make the cart clickable to open cart view with enhanced styling
        # Ensure consistent placement with back button in cart view
        self.cart_button = customtkinter.CTkButton(
            header_frame,
            text="🛒 Cart: 0 items",
            command=self.view_cart,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            corner_radius=8,  
            height=36,
            width=130  
        )
        self.cart_button.pack(side="right") 
        
        # Add a divider to match cart view
        divider = customtkinter.CTkFrame(self.root, height=1, fg_color=self.colors["border"])
        divider.pack(fill="x", padx=25, pady=(5, 15))
        
        # Update cart display when cart changes
        self.cart_service.add_listener(lambda _: self.update_cart_display())
        
    def update_cart_display(self):
        try:
            total_items = self.cart_service.get_total_items()
            
            # Check if button still exists to avoid errors
            if hasattr(self, 'cart_button') and self.cart_button.winfo_exists():
                self.cart_button.configure(text=f"🛒 Cart: {total_items} items")
                
                # Change button appearance if cart has items
                if total_items > 0:
                    self.cart_button.configure(fg_color=self.colors["success"], hover_color="#2D9300")
                else:
                    self.cart_button.configure(fg_color=self.colors["primary"], hover_color=self.colors["secondary"])
        except Exception as e:
            print(f"Error updating cart display: {e}")
        
    def view_cart(self):
        # Call the callback to show the cart view
        if self.on_view_cart:
            self.on_view_cart()
        
    def _create_filter_buttons(self):
        # Remove the redundant divider - we already have one from the header
        
        # Category title
        category_label = customtkinter.CTkLabel(
            self.root, 
            text="Categories", 
            font=customtkinter.CTkFont(size=18, weight="bold")  # Match section title sizes
        )
        category_label.pack(anchor="w", padx=25, pady=(0, 10))
        
        filter_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        filter_frame.pack(pady=(0, 15), padx=25, fill="x")  # Match padding
        
        categories = self.menu_service.get_categories()
        self.selected_category = tkinter.StringVar(value="All")
        
        segmented_button = customtkinter.CTkSegmentedButton(
            filter_frame,
            values=categories,
            variable=self.selected_category,
            command=self.filter_items,
            font=customtkinter.CTkFont(size=13),
            selected_color=self.colors["accent"],
            selected_hover_color="#E67D2D",
            unselected_color=self.colors["card_bg"],
            unselected_hover_color=self.colors["hover"],
            height=36,
            corner_radius=8
        )
        segmented_button.pack(fill="x")
        
    def _create_scrollable_frame(self):
        # Menu items title
        items_label = customtkinter.CTkLabel(
            self.root, 
            text="Menu Items", 
            font=customtkinter.CTkFont(size=18, weight="bold"),  # Match section title sizes
            anchor="w"  # Match anchor style
        )
        items_label.pack(anchor="w", padx=25, pady=(5, 10))
        
        # Increase height to match cart view's expanded size
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.root, 
            corner_radius=12,
           
            height=300  # Match cart view height
        )
        self.scrollable_frame.pack(padx=25, pady=(0, 20), fill="both", expand=True)
        
    def filter_items(self, category):
        # Clear image label references for the old view
        self.image_labels = {}
        
        # Clear current items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get filtered items
        filtered_items = self.menu_service.get_items_by_category(category)
        
        # Show message if no items
        if not filtered_items:
            no_items_label = customtkinter.CTkLabel(
                self.scrollable_frame, 
                text=f"No items available in {category} category",
                font=customtkinter.CTkFont(size=14),
                text_color=self.colors["text_secondary"]
            )
            no_items_label.pack(pady=30)
            return
            
        # Create new menu items in a grid layout
        for i, item in enumerate(filtered_items):
            self._create_item_widget(item)
    
    def _load_image_from_url(self, url, size=(120, 120), label_id=None):
        """Load an image from a URL using the image cache service"""
        def update_callback(image):
            # This callback is called when an image is loaded
            if label_id and label_id in self.image_labels and hasattr(self, 'root') and self.root.winfo_exists():
                try:
                    label = self.image_labels[label_id]
                    if label.winfo_exists():
                        print(f"Updating label with image: {url}")
                        label.configure(image=image)
                        self.root.update_idletasks()
                except Exception as e:
                    print(f"Error updating image in callback: {e}")
        
        return self.image_cache.get_image(url, size, update_callback, self.placeholder_image)
    
    def _create_item_widget(self, item):
        # Create a card-like frame with shadow effect
        item_frame = customtkinter.CTkFrame(
            self.scrollable_frame, 
            corner_radius=12,
            fg_color=self.colors["card_bg"],
            border_width=1,
            border_color=("#E0E0E0", "#3A3A3A")
        )
        item_frame.pack(fill="x", padx=5, pady=4)
        
        # Configure grid for flexible layout
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Generate a unique ID for this image label
        label_id = f"img_{item['name']}_{id(item)}"
        
        # Item image with rounded corners and proper aspect ratio
        if "image_url" in item:
            item_image = self._load_image_from_url(item["image_url"], size=(120, 120), label_id=label_id)
        else:
            item_image = self.placeholder_image
        
        # Store image widget reference for later updates
        image_container = customtkinter.CTkFrame(
            item_frame, 
            fg_color="transparent",
            width=120, 
            height=120
        )
        image_container.grid(row=0, column=0, padx=(15, 15), pady=15, sticky="w")
        
        image_label = customtkinter.CTkLabel(
            image_container, 
            image=item_image, 
            text=""
        )
        image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Store the label reference for later updates
        if "image_url" in item:
            self.image_labels[label_id] = image_label
        
        # Item information with better text hierarchy
        info_frame = customtkinter.CTkFrame(item_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=15)
        
        # Item name
        item_name = customtkinter.CTkLabel(
            info_frame, 
            text=item["name"], 
            font=customtkinter.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        item_name.pack(anchor="w", pady=(0, 3))

        # Food type label (veg, non-veg, jain)
        food_types = set([cat.lower() for cat in item.get("category", [])])
        food_type_label = None
        if "veg" in food_types:
            food_type_label = customtkinter.CTkLabel(
                info_frame,
                text="Veg",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#38B000",
                fg_color="#E6FFE6",
                corner_radius=6,
                padx=8,
                pady=2
            )
        elif "non veg" in food_types:
            food_type_label = customtkinter.CTkLabel(
                info_frame,
                text="Non Veg",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#D7263D",
                fg_color="#FFE6E6",
                corner_radius=6,
                padx=8,
                pady=2
            )
        elif "jain" in food_types:
            food_type_label = customtkinter.CTkLabel(
                info_frame,
                text="Jain",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#FF8C32",
                fg_color="#FFF5E6",
                corner_radius=6,
                padx=8,
                pady=2
            )
        if food_type_label:
            food_type_label.pack(anchor="w", pady=(0, 4))
        
        # Price tag with accent color
        price_tag = customtkinter.CTkLabel(
            info_frame, 
            text=item["price"],
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=self.colors["accent"],
            anchor="w"
        )
        price_tag.pack(anchor="w", pady=(0, 8))
        
        # Description with lighter color
        desc_label = customtkinter.CTkLabel(
            info_frame, 
            text=item["description"], 
            font=customtkinter.CTkFont(size=13),
            text_color=self.colors["text_secondary"],
            anchor="w",
            wraplength=400
        )
        desc_label.pack(anchor="w")
        
        # Add to cart button or quantity selector
        quantity = self.cart_service.get_quantity(item["name"])
        
        # Action container at the right side
        action_container = customtkinter.CTkFrame(
            item_frame, 
            fg_color="transparent",
            width=100
        )
        action_container.grid(row=0, column=2, padx=(0, 30), pady=15, sticky="e")
        
        if quantity > 0:
            self._create_quantity_selector(action_container, item["name"])
        else:
            add_btn = customtkinter.CTkButton(
                action_container, 
                text="Add to Cart",
                font=customtkinter.CTkFont(size=13, weight="bold"),
                width=100,
                height=36,
                fg_color=self.colors["primary"],
                hover_color=self.colors["secondary"],
                corner_radius=8,
                command=lambda name=item["name"]: self._add_initial(name, action_container)
            )
            add_btn.pack(pady=5)
            
    def _create_quantity_selector(self, frame, item_name):
        """Create a quantity selector with plus/minus buttons"""
        frame.destroy_children() if hasattr(frame, "destroy_children") else [child.destroy() for child in frame.winfo_children()]
        
        selector_frame = customtkinter.CTkFrame(frame, corner_radius=8)
        
        minus_btn = customtkinter.CTkButton(
            selector_frame, 
            text="−", 
            width=32,
            height=32,
            fg_color=self.colors["primary"],
            text_color=("white", "white"),
            hover_color=self.colors["secondary"],
            font=customtkinter.CTkFont(size=16, weight="bold"),
            corner_radius=8,
            command=lambda: self._update_quantity(item_name, -1, selector_frame)
        )
        minus_btn.pack(side="left", padx=(3, 0), pady=3)
        
        current_qty = self.cart_service.get_quantity(item_name)
        qty_label = customtkinter.CTkLabel(
            selector_frame, 
            text=str(current_qty), 
            width=32,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=("white", "white")
        )
        qty_label.pack(side="left")
        
        plus_btn = customtkinter.CTkButton(
            selector_frame, 
            text="+", 
            width=32,
            height=32,
            fg_color=self.colors["primary"],
            text_color=("white", "white"),
            hover_color=self.colors["secondary"],
            font=customtkinter.CTkFont(size=16, weight="bold"),
            corner_radius=8,
            command=lambda: self._update_quantity(item_name, 1, selector_frame)
        )
        plus_btn.pack(side="left", padx=(0, 3), pady=3)
        
        selector_frame.pack(pady=5)
        return selector_frame
    
    def _update_quantity(self, item_name, delta, container):
        try:
            current_qty = self.cart_service.get_quantity(item_name)
            new_qty = current_qty + delta
            
            if new_qty <= 0:
                # Switch back to Add button
                if container.winfo_exists():
                    container.destroy()
                    
                    if hasattr(container, 'master') and container.master.winfo_exists():
                        add_btn = customtkinter.CTkButton(
                            container.master, 
                            text="Add to Cart",
                            font=customtkinter.CTkFont(size=13, weight="bold"),
                            width=100,
                            height=36,
                            fg_color=self.colors["primary"],
                            hover_color=self.colors["secondary"],
                            corner_radius=8,
                            command=lambda: self._add_initial(item_name, container.master)
                        )
                        add_btn.pack(pady=5)
                self.cart_service.update_quantity(item_name, 0)
            else:
                self.cart_service.update_quantity(item_name, new_qty)
                # Update quantity label
                if container.winfo_exists():
                    children = container.winfo_children()
                    if len(children) > 1 and isinstance(children[1], customtkinter.CTkLabel):
                        children[1].configure(text=str(new_qty))
        except Exception as e:
            print(f"Error updating item quantity: {e}")
    
    def _add_initial(self, item_name, parent):
        # Replace Add button with quantity selector
        for widget in parent.winfo_children():
            if isinstance(widget, customtkinter.CTkButton) and "Add" in widget.cget("text"):
                widget.destroy()
        
        self.cart_service.add_item(item_name)
        self._create_quantity_selector(parent, item_name)