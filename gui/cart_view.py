import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import os
import webbrowser
from PIL import Image, ImageDraw
from services.invoice_service import InvoiceGenerator
import requests
import qrcode

class CartView:
    def __init__(self, root, cart_service, menu_service, on_back_to_menu=None):
        self.root = root
        self.cart_service = cart_service
        self.menu_service = menu_service
        self.on_back_to_menu = on_back_to_menu
        self.is_destroyed = False
        
        self.colors = {
            "primary": "#4D77FF",
            "secondary": "#5C77E6",
            "accent": "#FF8C32",
            "success": "#38B000",
            "danger": "#E63946",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "card_bg": ("#FFFFFF", "#2B2B2B"),
            "hover": ("#E6E6E6", "#3A3A3A"),
            "border": ("#E0E0E0", "#3A3A3A") 
        }
        
        # Create a main frame for cart
        self.main_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Build the UI
        self._create_header()
        self._create_cart_content()
        self._create_special_instructions()
        self._create_summary()
        self._create_buttons()
        
        # Update cart items display
        self.update_cart_display()
        
        # Listen for cart updates using a safe mechanism
        self.listener_id = self.cart_service.add_listener(self._on_cart_update)

        # Listen for menu updates (if menu changes, update cart view)
        self.menu_listener_id = self.menu_service.add_listener(self._on_menu_update)
    
    def _on_cart_update(self, _):
        """Wrapper method to safely update cart display"""
        # Only update if the view still exists
        if not self.is_destroyed and hasattr(self, 'cart_frame'):
            # Use tkinter's after method to safely update from event loop
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                self.main_frame.after(10, self.update_cart_display)
    
    def _on_menu_update(self, _):
        """Update cart display if menu changes (e.g., price/item updates)"""
        if not self.is_destroyed and hasattr(self, 'cart_frame'):
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                self.main_frame.after(10, self.update_cart_display)
    
    def _create_header(self):
        """Create the header section with title and back button"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        header_frame.pack(fill="x", padx=25, pady=(20, 15))
        
        # Cart title - now on the left side
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Your Cart 🛒", 
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(side="left")
         
        # Back button with icon and hover effect - now on the right side
        back_button = ctk.CTkButton(
            header_frame, 
            text="Back to Menu", 
            command=self._on_back_button_click,
            width=130,
            height=36,
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        back_button.pack(side="right" )
        
        # Add a divider
        divider = ctk.CTkFrame(self.main_frame, height=1, fg_color=self.colors["border"])
        divider.pack(fill="x", padx=25, pady=(5, 15))
    
    def _create_empty_cart_image(self):
        """Create a simple empty cart icon"""
        # Create a blank image
        img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple cart icon
        cart_color = self.colors["text_secondary"]
        # Draw cart body
        draw.rectangle((20, 50, 80, 80), outline=cart_color, width=2)
        # Draw cart handle
        draw.arc((15, 25, 45, 55), 180, 270, fill=cart_color, width=2)
        # Draw wheels
        draw.ellipse((25, 75, 35, 85), outline=cart_color, width=2)
        draw.ellipse((65, 75, 75, 85), outline=cart_color, width=2)
        
        # Convert to CTkImage
        return ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
    
    def _create_cart_content(self):
        """Create the scrollable frame to display cart items"""
        # Create a container frame that will hold both the title and scrollable content
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=25)
        
        # Section title
        section_title = ctk.CTkLabel(
            self.content_container,
            text="Order Items",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        section_title.pack(anchor="w", pady=(0, 10))
        
        # Label for empty cart with improved styling
        self.empty_cart_label = ctk.CTkLabel(
            self.content_container,
            text="Your cart is empty. Go back to the menu to add some items.",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["text_secondary"],
            compound="top",
            pady=20
        )
        
        # Create a frame that will contain the scrollable frame - this allows for proper expanding
        self.cart_container = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.cart_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create scrollable frame with rounded corners for cart items
        self.cart_frame = ctk.CTkScrollableFrame(
            self.cart_container, 
            corner_radius=12,
            fg_color=self.colors["card_bg"],
            border_width=1,
            border_color=self.colors["border"]
        )
        self.cart_frame.pack(fill="both", expand=True)
        
        # Create table header with distinct styling
        self.header_frame = ctk.CTkFrame(self.cart_frame, fg_color="transparent", height=40)
        self.header_frame.pack(fill="x", pady=(5, 10))
        
        # Configure grid columns with fixed minimum widths for consistency
        self.header_frame.grid_columnconfigure(0, weight=6, minsize=150)  # Item name
        self.header_frame.grid_columnconfigure(1, weight=2, minsize=70)   # Price
        self.header_frame.grid_columnconfigure(2, weight=2, minsize=100)  # Quantity
        self.header_frame.grid_columnconfigure(3, weight=2, minsize=70)   # Total
        self.header_frame.grid_columnconfigure(4, weight=0, minsize=40)   # Remove button

        # Create styled headers with consistent text alignment
        headers = ["Item", "Price", "Quantity", "Total", ""]
        alignments = ["w", "center", "center", "e", "center"]  # Proper anchor for each column
        sticky_values = ["w", "ew", "n", "e", "ns"]  # Proper sticky for positioning
        
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.header_frame, 
                text=header, 
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor=alignments[i]  
            ).grid(row=0, column=i, 
                sticky=sticky_values[i],  # Consistent sticky values
                padx=10, 
                pady=5)
        
        # Create a container for cart items
        self.items_container = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        self.items_container.pack(fill="x", expand=True)
    
    def _create_special_instructions(self):
        """Create the special instructions section"""
        # Make the special instructions section take less vertical space when cart is large
        instructions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        instructions_frame.pack(fill="x", padx=25, pady=10)
        
        # Title with icon
        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text="✏️ Special Instructions",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        instructions_label.pack(anchor="w", pady=(0, 5))  # Reduced padding
        
        # Text box with improved styling - reduced height
        self.instructions_text = ctk.CTkTextbox(
            instructions_frame,
            height=60,  # Reduced height
            wrap="word",
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"]
        )
        self.instructions_text.pack(fill="x")
        
        # Add a default instruction text that can be cleared by user
        default_text = "Add any special requirements or instructions (e.g., allergies, spice level, etc.)"
        self.instructions_text.insert("1.0", default_text)
        
        # Add focus event to clear the default text when user clicks
        self.instructions_text.bind("<FocusIn>", lambda e: self._clear_default_text(default_text))
    
    def _clear_default_text(self, default_text):
        """Clear the default text when user focuses on the textbox"""
        current_text = self.instructions_text.get("1.0", "end-1c")
        if current_text.strip() == default_text.strip():
            self.instructions_text.delete("1.0", "end")
    
    def _create_summary(self):
        """Create the order summary section with subtotal, tax, and total"""
        # Reduce vertical space for summary
        summary_title = ctk.CTkLabel(
            self.main_frame,
            text="Order Summary",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        summary_title.pack(anchor="w", padx=25, pady=(10, 5))  # Reduced padding
        
        # Summary card with border
        self.summary_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=12,
            fg_color=self.colors["card_bg"],
            border_width=1,
            border_color=self.colors["border"]
        )
        self.summary_frame.pack(fill="x", padx=25, pady=(0, 15))
        
        # Create grid layout for summary
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=0)
        
        # Subtotal row
        ctk.CTkLabel(
            self.summary_frame, 
            text="Subtotal:", 
            font=ctk.CTkFont(size=14),
            anchor="e"
        ).grid(row=0, column=0, sticky="e", padx=15, pady=(15, 5))
        
        self.subtotal_label = ctk.CTkLabel(
            self.summary_frame, 
            text="₹0.00", 
            font=ctk.CTkFont(size=14),
            anchor="e"
        )
        self.subtotal_label.grid(row=0, column=1, sticky="e", padx=15, pady=(15, 5))
        
        # Tax row
        ctk.CTkLabel(
            self.summary_frame, 
            text="Tax (5%):", 
            font=ctk.CTkFont(size=14),
            anchor="e"
        ).grid(row=1, column=0, sticky="e", padx=15, pady=5)
        
        self.tax_label = ctk.CTkLabel(
            self.summary_frame, 
            text="₹0.00", 
            font=ctk.CTkFont(size=14),
            anchor="e"
        )
        self.tax_label.grid(row=1, column=1, sticky="e", padx=15, pady=5)
        
        # Separator
        separator = ctk.CTkFrame(self.summary_frame, height=1, fg_color=self.colors["border"])
        separator.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=15)
        
        # Total row
        ctk.CTkLabel(
            self.summary_frame, 
            text="Total:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="e"
        ).grid(row=3, column=0, sticky="e", padx=15, pady=(5, 15))
        
        self.total_label = ctk.CTkLabel(
            self.summary_frame, 
            text="₹0.00", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["accent"],
            anchor="e"
        )
        self.total_label.grid(row=3, column=1, sticky="e", padx=15, pady=(5, 15))
    
    def _create_buttons(self):
        """Create the action buttons for checkout and clear cart"""
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=25, pady=(0, 25))
        
        clear_cart_button = ctk.CTkButton(
            button_frame, 
            text="Clear Cart", 
            command=self._clear_cart,
            fg_color=self.colors["danger"],
            hover_color="#C42B36",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )
        clear_cart_button.pack(side="left", padx=5)
        
        self.checkout_button = ctk.CTkButton(
            button_frame, 
            text="Checkout", 
            command=self._checkout,
            fg_color=self.colors["success"],
            hover_color="#2D9300",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )
        self.checkout_button.pack(side="right", padx=5)
    
    def update_cart_display(self):
        """Update the cart items display"""
        # Safety check - only update if cart frame exists
        if not hasattr(self, 'cart_frame'):
            return
            
        try:
            # Check if cart frame widget still exists
            if not self.cart_frame.winfo_exists():
                return
                
            cart_items = self.cart_service.get_all_items()
            
            # Check if cart is empty
            if not cart_items:
                self.empty_cart_label.pack(pady=50)
                self.cart_container.pack_forget()  # Hide the container instead of just the frame
                if hasattr(self, 'checkout_button') and self.checkout_button.winfo_exists():
                    self.checkout_button.configure(state="disabled")
                self.update_summary(0)
                return
            else:
                self.empty_cart_label.pack_forget()
                # Make sure container is visible and properly expanded
                self.cart_container.pack(fill="both", expand=True, pady=(0, 10))
                # Ensure the scrollable frame fills the container
                self.cart_frame.pack(fill="both", expand=True)
                if hasattr(self, 'checkout_button') and self.checkout_button.winfo_exists():
                    self.checkout_button.configure(state="normal")
            
            # Check if items container exists, recreate if needed
            if not hasattr(self, 'items_container') or not self.items_container.winfo_exists():
                self.items_container = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
                self.items_container.pack(fill="x", expand=True)
            
            # Clear all existing items from the container to prevent duplicates
            for widget in self.items_container.winfo_children():
                widget.destroy()
            
            # Display cart items
            subtotal = 0
            current_item_frames = {}
            
            for i, (item_name, quantity) in enumerate(cart_items.items()):
                # Find the menu item details
                menu_item = next((item for item in self.menu_service.get_all_items() 
                                if item["name"] == item_name), None)
                
                if menu_item:
                    # Create a frame for this item with alternating background for better readability
                    item_frame = ctk.CTkFrame(
                        self.items_container, 
                        fg_color="transparent" if i % 2 == 0 else self.colors["hover"],
                    )
                    item_frame.pack(fill="x", pady=1)
                    current_item_frames[item_name] = item_frame
                    
                    # Configure grid layout with the same column configuration as header - EXACT MATCH
                    item_frame.grid_columnconfigure(0, weight=6, minsize=150)  # Item name
                    item_frame.grid_columnconfigure(1, weight=2, minsize=70)   # Price
                    item_frame.grid_columnconfigure(2, weight=2, minsize=100)  # Quantity
                    item_frame.grid_columnconfigure(3, weight=2, minsize=70)   # Total
                    item_frame.grid_columnconfigure(4, weight=0, minsize=40)   # Remove button
                    
                    # Item name with ellipsis for long names
                    name_label = ctk.CTkLabel(
                        item_frame, 
                        text=item_name,
                        font=ctk.CTkFont(size=14),
                        anchor="w"
                    )
                    name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
                    
                    # Item price - align right
                    price_text = menu_item["price"]
                    price_value = float(price_text.replace("₹", ""))
                    
                    ctk.CTkLabel(
                        item_frame, 
                        text=price_text,
                        font=ctk.CTkFont(size=14),
                        anchor="e",
                    ).grid(row=0, column=1, sticky="ew", padx=80, pady=10)
                    
                    # Quantity controls - create centered container
                    qty_container = ctk.CTkFrame(item_frame, fg_color="transparent")
                    qty_container.grid(row=0, column=2, sticky="ew", padx=10, pady=10)  # Centered vertically
                    
                    # Center the quantity controls within the frame
                    qty_frame = ctk.CTkFrame(qty_container, fg_color="transparent")
                    qty_frame.pack(expand=True)
                    
                    # Horizontally layout the quantity controls
                    minus_btn = ctk.CTkButton(
                        qty_frame, 
                        text="−", 
                        width=28, 
                        height=28,
                        fg_color=self.colors["primary"],
                        hover_color=self.colors["secondary"],
                        corner_radius=5,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        command=lambda name=item_name: self._update_quantity(name, -1)
                    )
                    minus_btn.pack(side="left", padx=2)
                    
                    qty_label = ctk.CTkLabel(
                        qty_frame, 
                        text=str(quantity),
                        width=30,
                        font=ctk.CTkFont(size=14),
                        anchor="center"
                    )
                    qty_label.pack(side="left", padx=2)
                    
                    plus_btn = ctk.CTkButton(
                        qty_frame, 
                        text="+", 
                        width=28, 
                        height=28,
                        fg_color=self.colors["primary"],
                        hover_color=self.colors["secondary"],
                        corner_radius=5,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        command=lambda name=item_name: self._update_quantity(name, 1)
                    )
                    plus_btn.pack(side="left", padx=2)
                    
                    # Store reference to quantity label for direct updates
                    if not hasattr(self, 'qty_labels'):
                        self.qty_labels = {}
                    self.qty_labels[item_name] = qty_label
                    
                    # Item total - align right consistently with header
                    item_total = price_value * quantity
                    subtotal += item_total
                    
                    ctk.CTkLabel(
                        item_frame, 
                        text=f"₹{item_total:.2f}",
                        font=ctk.CTkFont(size=14),
                        anchor="e"
                    ).grid(row=0, column=3, sticky="e", padx=10, pady=10)
                    
                    # Add remove button - centered
                    remove_container = ctk.CTkFrame(item_frame, fg_color="transparent")
                    remove_container.grid(row=0, column=4, sticky="ns", padx=10, pady=10)  # Centered vertically
                    
                    remove_btn = ctk.CTkButton(
                        remove_container, 
                        text="×", 
                        width=28, 
                        height=28,
                        fg_color=self.colors["danger"],
                        hover_color="#C42B36",
                        corner_radius=5,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        command=lambda name=item_name: self._remove_item(name)
                    )
                    remove_btn.pack(expand=True)
            
            # Store current item frames for reference
            self.item_frames = current_item_frames
            
            # Update the summary
            self.update_summary(subtotal)
        except Exception as e:
            print(f"Error in update_cart_display: {e}")
    
    def update_summary(self, subtotal):
        """Update the summary section with calculated values"""
        tax_rate = 0.05
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        # Safety check before updating
        if hasattr(self, 'subtotal_label') and self.subtotal_label.winfo_exists():
            self.subtotal_label.configure(text=f"₹{subtotal:.2f}")
        
        if hasattr(self, 'tax_label') and self.tax_label.winfo_exists():
            self.tax_label.configure(text=f"₹{tax:.2f}")
        
        if hasattr(self, 'total_label') and self.total_label.winfo_exists():
            self.total_label.configure(text=f"₹{total:.2f}")
    
    def _update_quantity(self, item_name, delta):
        """Update the quantity of an item in the cart"""
        try:
            current_qty = self.cart_service.get_quantity(item_name)
            new_qty = current_qty + delta
            
            if new_qty <= 0:
                self._remove_item(item_name)
            else:
                self.cart_service.update_quantity(item_name, new_qty)
                
                # Directly update quantity label for immediate feedback without redrawing
                if hasattr(self, 'qty_labels') and item_name in self.qty_labels:
                    qty_label = self.qty_labels[item_name]
                    if qty_label.winfo_exists():
                        qty_label.configure(text=str(new_qty))
                        
                        # Also update the item total display
                        if hasattr(self, 'item_frames') and item_name in self.item_frames:
                            item_frame = self.item_frames[item_name]
                            if item_frame.winfo_exists():
                                # Find menu item price
                                menu_item = next((item for item in self.menu_service.get_all_items() 
                                            if item["name"] == item_name), None)
                                if menu_item:
                                    price_value = float(menu_item["price"].replace("₹", ""))
                                    item_total = price_value * new_qty
                                    
                                    # Find and update total label (column 3)
                                    children = item_frame.grid_slaves(row=0, column=3)
                                    if children:
                                        total_label = children[0]
                                        total_label.configure(text=f"₹{item_total:.2f}")
                
                # Update summary without redrawing everything
                cart_items = self.cart_service.get_all_items()
                subtotal = sum(
                    float(next((item["price"].replace("₹", "") for item in self.menu_service.get_all_items() 
                           if item["name"] == item_name), 0)) * qty
                    for item_name, qty in cart_items.items()
                )
                self.update_summary(subtotal)
        except Exception as e:
            print(f"Error updating quantity: {e}")
    
    def _remove_item(self, item_name):
        """Remove an item from the cart"""
        self.cart_service.update_quantity(item_name, 0)
    
    def _clear_cart(self):
        """Clear all items from the cart"""
        self.cart_service.clear_cart()
        
        # Reset instructions text to default
        self.instructions_text.delete("1.0", "end")
        default_text = "Add any special requirements or instructions (e.g., allergies, spice level, etc.)"
        self.instructions_text.insert("1.0", default_text)
    
    def _checkout(self):
        """Process checkout and generate invoice, and send order to backend"""
        # Get special instructions
        special_instructions = self.instructions_text.get("1.0", "end-1c").strip()
        default_text = "Add any special requirements or instructions (e.g., allergies, spice level, etc.)"
        if special_instructions == default_text:
            special_instructions = ""

        # Prepare order data for backend
        cart_items = self.cart_service.get_all_items()
        order_items = []
        for item_name, qty in cart_items.items():
            menu_item = next((item for item in self.menu_service.get_all_items() if item["name"] == item_name), None)
            if menu_item:
                order_items.append({
                    "name": item_name,
                    "qty": qty,
                    "price": menu_item["price"]
                })
        subtotal = sum(float(item["price"].replace("₹", "")) * item["qty"] for item in order_items)
        tax = subtotal * 0.05
        total = subtotal + tax
        order_data = {
            "items": order_items,
            "special_instructions": special_instructions,
            "total": total
        }
        print("Order successfully.", order_data)
        # Send order to backend
        try:
            response = requests.post("http://127.0.0.1:5000/orders", json=order_data, timeout=5)
            if response.status_code == 201:
                print("Order sent to backend successfully.", order_data)
                order_id = response.json().get("order_id")
            else:
                print(f"Backend error: {response.text}")
                order_id = None
        except Exception as e:
            print(f"Failed to send order to backend: {e}")
            order_id = None

        if order_id is None:
            ctk.CTkLabel(self.main_frame, text="Order creation failed. Please try again.", font=ctk.CTkFont(size=14), text_color=self.colors["danger"]).pack(pady=10)
            return

        # Generate the invoice using the service
        invoice_service = InvoiceGenerator(
            cart_items=self.cart_service.get_all_items(),
            menu_service=self.menu_service,
            special_instructions=special_instructions,
            order_id=order_id
        )
        invoice_path = invoice_service.generate_invoice()

        # Generate static QR code (e.g., payment link or static text)
        qr_data = "upi://pay?pa=demo@upi&pn=Canteen&am={:.2f}&cu=INR".format(order_data["total"])
        qr_img = qrcode.make(qr_data)
        qr_path = os.path.join(os.getcwd(), "static_qr.png")
        qr_img.save(qr_path)

        self._show_checkout_success(invoice_path, qr_path, order_id)

    def _show_checkout_success(self, invoice_path, qr_path=None, order_id=None):
        """Show checkout success dialog with QR code, poll for payment, then show invoice button"""
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Order Confirmed")
        success_window.geometry("450x420")
        success_window.transient(self.root)
        success_window.grab_set()
        success_window.update_idletasks()
        width = success_window.winfo_width()
        height = success_window.winfo_height()
        x = (success_window.winfo_screenwidth() // 2) - (width // 2)
        y = (success_window.winfo_screenheight() // 2) - (height // 2)
        success_window.geometry(f"{width}x{height}+{x}+{y}")

        frame = ctk.CTkFrame(success_window, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="✅ Order Confirmed!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["success"]
        ).pack(pady=(20, 15))
        ctk.CTkLabel(
            frame,
            text="Your order has been confirmed. Please scan the QR code to pay.",
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=5)
        

        # Show QR code if available
        self.qr_label = None  # Store reference to QR/tick label
        if qr_path and os.path.exists(qr_path):
            from PIL import ImageTk
            qr_img = Image.open(qr_path).resize((120, 120))
            qr_photo = ctk.CTkImage(light_image=qr_img, dark_image=qr_img, size=(120, 120))
            self.qr_label = ctk.CTkLabel(frame, text="Scan to Pay", font=ctk.CTkFont(size=14, weight="bold"), image=qr_photo, compound="top")
            self.qr_label.pack(pady=10)

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=15)

        view_invoice_btn = ctk.CTkButton(
            button_frame,
            text="View Invoice",
            command=lambda: self._open_invoice(invoice_path),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            corner_radius=8,
            state="disabled"
        )
        view_invoice_btn.pack(side="left", padx=10)

        close_btn = ctk.CTkButton(
            button_frame,
            text="Done",
            command=lambda: [success_window.destroy(), self._clear_cart(), self._on_back_button_click()],
            fg_color=self.colors["success"],
            hover_color="#2D9300",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            corner_radius=8,
            state="disabled"
        )
        close_btn.pack(side="right", padx=10)

        def create_tick_image(size=120, bg_color="#38B000", fg_color="white", thickness_ratio=0.12):
            """
            Creates a professional-looking success tick/check mark icon.
            
            Args:
                size (int): Size of the image in pixels
                bg_color (str): Background circle color in hex
                fg_color (str): Foreground tick color in hex
                thickness_ratio (float): Thickness of the tick relative to size
                
            Returns:
                PIL.Image: The generated tick image
            """
            # Create transparent background
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Calculate padding for better appearance
            padding = size * 0.1
            effective_size = size - (2 * padding)
            
            # Draw the outer circle with anti-aliasing
            circle_bbox = [
                (padding, padding),
                (size - padding, size - padding)
            ]
            draw.ellipse(circle_bbox, fill=bg_color)
            
            # Calculate tick thickness
            thickness = int(size * thickness_ratio)
            
            # For a more professional look, let's create a slightly smoother check mark
            # by using multiple points instead of just three
            
            # Start point (left side of check)
            start_x = padding + (effective_size * 0.27)
            start_y = padding + (effective_size * 0.54)
            
            # Middle point (bottom of check)
            mid_x = padding + (effective_size * 0.45)
            mid_y = padding + (effective_size * 0.70)
            
            # Control point for smooth curve
            ctrl_x = padding + (effective_size * 0.40)
            ctrl_y = padding + (effective_size * 0.65)
            
            # End point (right side of check, top)
            end_x = padding + (effective_size * 0.75)
            end_y = padding + (effective_size * 0.32)
            
            # Enhanced check mark with more points for smoother appearance
            tick_points = [
                (start_x, start_y),                       # Start point
                (start_x + size*0.05, start_y + size*0.05),  # Control point 1
                (ctrl_x, ctrl_y),                         # Control point 2
                (mid_x, mid_y),                           # Middle point
                (mid_x + size*0.08, mid_y - size*0.03),   # Control point 3
                (mid_x + size*0.16, mid_y - size*0.12),   # Control point 4
                (end_x, end_y)                            # End point
            ]
            
            # Draw the tick with rounded caps
            for i in range(len(tick_points) - 1):
                draw.line(
                    [tick_points[i], tick_points[i+1]], 
                    fill=fg_color, 
                    width=thickness, 
                    joint="curve"
                )
            
            # Add subtle inner highlight for 3D effect
            highlight_thickness = max(1, int(thickness * 0.25))
            highlight_color = "#FFFFFF80"  # Semi-transparent white
            
            # Draw highlight on the top edge of the tick
            for i in range(len(tick_points) - 2):
                highlight_points = [
                    (tick_points[i][0] - 1, tick_points[i][1] - 1),
                    (tick_points[i+1][0] - 1, tick_points[i+1][1] - 1)
                ]
                draw.line(
                    highlight_points,
                    fill=highlight_color,
                    width=highlight_thickness
                )
            
            return img

        def poll_payment():
            try:
                resp = requests.get(f"http://127.0.0.1:5000/orders/{order_id}/status", timeout=3)
                if resp.status_code == 200 and resp.json().get("payment_status") == "paid":
                    view_invoice_btn.configure(state="normal")
                    close_btn.configure(state="normal")
                    # Replace QR code with tick image
                    if self.qr_label is not None:
                        tick_img = create_tick_image()
                        tick_photo = ctk.CTkImage(light_image=tick_img, dark_image=tick_img, size=(120, 120))
                        self.qr_label.configure(image=tick_photo, text="Payment Successful!", font=ctk.CTkFont(size=16, weight="bold"), compound="top")
                        self.qr_label.image = tick_photo  # Prevent garbage collection
                    ctk.CTkLabel(frame, text="Payment received! You can now view your invoice.", font=ctk.CTkFont(size=14), text_color=self.colors["success"]).pack(pady=5)
                    return
            except Exception as e:
                print(f"Polling error: {e}")
            # Poll every 2 seconds
            success_window.after(2000, poll_payment)

        poll_payment()
    
    def _open_invoice(self, invoice_path):
        """Open the invoice in the default PDF viewer"""
        if os.path.exists(invoice_path):
            webbrowser.open(invoice_path)
        else:
            print("Invoice file not found.")
    
    def _on_back_button_click(self):
        """Handle back button click"""
        if self.on_back_to_menu:
            self.on_back_to_menu()
    
    def destroy(self):
        """Destroy the cart view and clean up listeners"""
        self.is_destroyed = True
        if hasattr(self, 'listener_id'):
            self.cart_service.remove_listener(self.listener_id)
        if hasattr(self, 'menu_listener_id'):
            self.menu_service.remove_listener(self.menu_listener_id)
        self.main_frame.destroy()

