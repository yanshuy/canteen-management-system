import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import os
import webbrowser
from PIL import Image, ImageDraw
from services.invoice_service import InvoiceGenerator

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
    
    def _on_cart_update(self, _):
        """Wrapper method to safely update cart display"""
        # Only update if the view still exists
        if not self.is_destroyed and hasattr(self, 'cart_frame'):
            # Use tkinter's after method to safely update from event loop
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
        header_frame = ctk.CTkFrame(self.cart_frame, fg_color="transparent", height=40)
        header_frame.pack(fill="x", pady=(5, 10))
        
        # Configure grid columns for proper alignment
        header_frame.grid_columnconfigure(0, weight=4)  # Item name - slightly reduced
        header_frame.grid_columnconfigure(1, weight=2)  # Price
        header_frame.grid_columnconfigure(2, weight=2)  # Quantity
        header_frame.grid_columnconfigure(3, weight=2)  # Total
        header_frame.grid_columnconfigure(4, weight=1)  # Remove button

        # Create styled headers with consistent text alignment
        headers = ["Item", "Price", "Quantity", "Total", ""]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w" if i == 0 else "e"  # Left align for Item, right align for others
            ).grid(row=0, column=i, 
                sticky="w" if i == 0 else "e",  # Ensure proper sticky alignment 
                padx=10, 
                pady=5)
    
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
            text="Checkout & Generate Invoice", 
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
                
            # Clear existing items (except header)
            children = self.cart_frame.winfo_children()
            if children:
                header = children[0] if len(children) > 0 else None
                
                for widget in children:
                    if widget != header:
                        widget.destroy()
            
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
            
            # Display cart items
            subtotal = 0
            
            # Use a dictionary to store item references
            self.item_frames = {}
            
            for i, (item_name, quantity) in enumerate(cart_items.items()):
                # Find the menu item details
                menu_item = next((item for item in self.menu_service.get_all_items() 
                                if item["name"] == item_name), None)
                
                if menu_item:
                    # Create a frame for this item with alternating background for better readability
                    item_frame = ctk.CTkFrame(
                        self.cart_frame, 
                        fg_color="transparent" if i % 2 == 0 else self.colors["hover"]
                    )
                    item_frame.pack(fill="x", pady=1)
                    
                    # Configure grid layout
                    item_frame.grid_columnconfigure(0, weight=4)  # Item name
                    item_frame.grid_columnconfigure(1, weight=2)  # Price
                    item_frame.grid_columnconfigure(2, weight=2)  # Quantity
                    item_frame.grid_columnconfigure(3, weight=2)  # Total
                    item_frame.grid_columnconfigure(4, weight=1)  # Remove button
                    
                    # Item name
                    ctk.CTkLabel(
                        item_frame, 
                        text=item_name,
                        font=ctk.CTkFont(size=14),
                        anchor="w"
                    ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
                    
                    # Item price
                    price_text = menu_item["price"]
                    price_value = float(price_text.replace("₹", ""))
                    
                    ctk.CTkLabel(
                        item_frame, 
                        text=price_text,
                        font=ctk.CTkFont(size=14),
                        anchor="e"
                    ).grid(row=0, column=1, sticky="e", padx=10, pady=10)
                    
                    # Quantity controls - using a safer approach to avoid widget destruction issues
                    qty_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                    qty_frame.grid(row=0, column=2, sticky="e", padx=10, pady=10)
                    
                    # Store reference in dictionary
                    self.item_frames[item_name] = {
                        "frame": qty_frame,
                        "quantity": quantity
                    }
                    
                    # Use lambda functions with default arguments to capture values properly
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
                        font=ctk.CTkFont(size=14)
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
                    
                    # Item total
                    item_total = price_value * quantity
                    subtotal += item_total
                    
                    ctk.CTkLabel(
                        item_frame, 
                        text=f"₹{item_total:.2f}",
                        font=ctk.CTkFont(size=14),
                        anchor="e"
                    ).grid(row=0, column=3, sticky="e", padx=10, pady=10)
                    
                    # Add remove button - use direct lambda with name arg
                    remove_btn = ctk.CTkButton(
                        item_frame, 
                        text="×", 
                        width=28, 
                        height=28,
                        fg_color=self.colors["danger"],
                        hover_color="#C42B36",
                        corner_radius=5,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        command=lambda name=item_name: self._remove_item(name)
                    )
                    remove_btn.grid(row=0, column=4, padx=10, pady=10)
            
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
                
                # Directly update quantity display for immediate feedback
                if item_name in self.item_frames:
                    qty_frame = self.item_frames[item_name]["frame"]
                    if qty_frame.winfo_exists():
                        # Update the label (second child)
                        children = qty_frame.winfo_children()
                        if len(children) > 1 and isinstance(children[1], ctk.CTkLabel):
                            children[1].configure(text=str(new_qty))
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
        """Process checkout and generate invoice"""
        # Get special instructions
        special_instructions = self.instructions_text.get("1.0", "end-1c").strip()
        
        # Check if it's the default text and remove it if it is
        default_text = "Add any special requirements or instructions (e.g., allergies, spice level, etc.)"
        if special_instructions == default_text:
            special_instructions = ""
        
        # Generate the invoice using the service
        invoice_service = InvoiceGenerator(
            cart_items=self.cart_service.get_all_items(),
            menu_service=self.menu_service,
            special_instructions=special_instructions
        )
        
        invoice_path = invoice_service.generate_invoice()
        
        # Show success message
        self._show_checkout_success(invoice_path)
    
    def _show_checkout_success(self, invoice_path):
        """Show checkout success dialog with options to view invoice"""
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Order Confirmed")
        success_window.geometry("450x320")
        success_window.transient(self.root)  # Set as transient to main window
        success_window.grab_set()  # Make it modal
        
        # Center window
        success_window.update_idletasks()
        width = success_window.winfo_width()
        height = success_window.winfo_height()
        x = (success_window.winfo_screenwidth() // 2) - (width // 2)
        y = (success_window.winfo_screenheight() // 2) - (height // 2)
        success_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create a styled frame with padding
        frame = ctk.CTkFrame(success_window, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Success message with check mark icon
        ctk.CTkLabel(
            frame,
            text="✅ Order Confirmed!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["success"]
        ).pack(pady=(20, 25))
        
        ctk.CTkLabel(
            frame,
            text="Your order has been confirmed and the invoice has been generated.",
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=5)
        
        ctk.CTkLabel(
            frame,
            text="Thank you for your order!",
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=5)
        
        # Buttons for invoice actions with improved styling
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        view_invoice_btn = ctk.CTkButton(
            button_frame,
            text="View Invoice",
            command=lambda: self._open_invoice(invoice_path),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            corner_radius=8
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
            corner_radius=8
        )
        close_btn.pack(side="right", padx=10)
    
    def _open_invoice(self, invoice_path):
        """Open the invoice file with the default system viewer"""
        try:
            # Convert to absolute path if needed
            if not os.path.isabs(invoice_path):
                invoice_path = os.path.join(os.getcwd(), invoice_path)
            
            # Open the invoice with the default application
            webbrowser.open(f"file://{invoice_path}")
        except Exception as e:
            print(f"Error opening invoice: {e}")
    
    def _on_back_button_click(self):
        """Handle back button click"""
        # Mark as destroyed so we don't update after destruction
        self.is_destroyed = True
        
        # Remove our listener from cart service
        if hasattr(self, 'listener_id'):
            self.cart_service.remove_listener(self.listener_id)
            
        # Safely destroy the frame after a short delay to avoid callback issues
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            self.main_frame.after(50, self._safe_destroy)
    
    def _safe_destroy(self):
        """Safely destroy the main frame and call the back function"""
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            self.main_frame.destroy()
        
        # Call the callback to show menu
        if self.on_back_to_menu:
            self.on_back_to_menu()
    
    def show(self):
        """Show the cart view"""
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            self.main_frame.pack(fill="both", expand=True)

