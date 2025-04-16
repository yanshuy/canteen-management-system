import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from PIL import Image, ImageTk
from utils.colors import COLORS
from utils.widgets import Card

class AddItemsPage(tk.Frame):
    def __init__(self, parent, on_item_added=None):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # Callback for when item is added
        self.on_item_added = on_item_added
        
        # Initialize variables
        self.image_path = None
        self.image_preview = None
        
        # Page header
        self.header = tk.Frame(self, bg=COLORS["bg_main"], height=70)
        self.header.pack(fill=tk.X)
        
        self.title = tk.Label(
            self.header,
            text="Add New Item",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"]
        )
        self.title.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Content area
        self.content = tk.Frame(self, bg=COLORS["bg_main"])
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create main form card
        self.form_card = Card(self.content)
        self.form_card.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create form layout
        self.form_frame = tk.Frame(self.form_card, bg=COLORS["bg_card"])
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Two-column layout
        self.left_column = tk.Frame(self.form_frame, bg=COLORS["bg_card"])
        self.left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.right_column = tk.Frame(self.form_frame, bg=COLORS["bg_card"])
        self.right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Left column content - Item details
        self.create_left_column()
        
        # Right column content - Image upload
        self.create_right_column()
        
        # Form buttons at the bottom
        self.create_form_buttons()
    
    def create_left_column(self):
        # Item Name
        self.name_label = tk.Label(
            self.left_column,
            text="Item Name:",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.name_label.pack(fill=tk.X, pady=(0, 5))
        
        self.name_entry = tk.Entry(
            self.left_column,
            font=("Segoe UI", 11),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"]
        )
        self.name_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Category
        self.category_label = tk.Label(
            self.left_column,
            text="Category:",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.category_label.pack(fill=tk.X, pady=(0, 5))
        
        # Sample categories
        categories = ["South Indian", "North Indian", "Chinese", "Main Course", "Starters", "Dessert", "Beverages"]
        
        self.category_combobox = ttk.Combobox(
            self.left_column,
            values=categories,
            font=("Segoe UI", 11),
            state="readonly"
        )
        self.category_combobox.pack(fill=tk.X, pady=(0, 15), ipady=4)
        
        if categories:
            self.category_combobox.current(0)
        
        # Style the combobox
        self.style = ttk.Style()
        self.style.configure("TCombobox", 
                            fieldbackground=COLORS["bg_main"], 
                            background=COLORS["bg_main"])
        
        # Price
        self.price_label = tk.Label(
            self.left_column,
            text="Price (₹):",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.price_label.pack(fill=tk.X, pady=(0, 5))
        
        self.price_entry = tk.Entry(
            self.left_column,
            font=("Segoe UI", 11),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"]
        )
        self.price_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Old Price (optional)
        self.old_price_label = tk.Label(
            self.left_column,
            text="Old Price (₹) (Optional):",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.old_price_label.pack(fill=tk.X, pady=(0, 5))
        
        self.old_price_entry = tk.Entry(
            self.left_column,
            font=("Segoe UI", 11),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"]
        )
        self.old_price_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Stock Status
        self.stock_frame = tk.Frame(self.left_column, bg=COLORS["bg_card"])
        self.stock_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.stock_label = tk.Label(
            self.stock_frame,
            text="In Stock:",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"]
        )
        self.stock_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stock_var = tk.BooleanVar(value=True)
        self.stock_checkbox = tk.Checkbutton(
            self.stock_frame,
            variable=self.stock_var,
            bg=COLORS["bg_card"],
            activebackground=COLORS["bg_card"],
            selectcolor=COLORS["bg_main"]
        )
        self.stock_checkbox.pack(side=tk.LEFT)
    
    def create_right_column(self):
        # Image upload section
        self.image_label = tk.Label(
            self.right_column,
            text="Item Image:",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.image_label.pack(fill=tk.X, pady=(0, 10))
        
        # Image preview frame
        self.image_preview_frame = tk.Frame(
            self.right_column,
            bg=COLORS["border"],
            width=200,
            height=200,
            bd=1,
            relief=tk.SOLID
        )
        self.image_preview_frame.pack(pady=(0, 15))
        self.image_preview_frame.pack_propagate(False)
        
        # Default preview text
        self.preview_label = tk.Label(
            self.image_preview_frame,
            text="No Image Selected",
            font=("Segoe UI", 11),
            bg=COLORS["border"],
            fg=COLORS["text_secondary"]
        )
        self.preview_label.pack(expand=True)
        
        # Upload button
        self.upload_button = tk.Button(
            self.right_column,
            text="Choose Image",
            font=("Segoe UI", 11),
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2",
            activebackground=COLORS["primary_hover"],
            activeforeground=COLORS["text_light"],
            command=self.choose_image
        )
        self.upload_button.pack(fill=tk.X, pady=(0, 15))
        
        # Description text area
        self.description_label = tk.Label(
            self.right_column,
            text="Description (Optional):",
            font=("Segoe UI", 12),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.description_label.pack(fill=tk.X, pady=(0, 5))
        
        self.description_text = tk.Text(
            self.right_column,
            font=("Segoe UI", 11),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            height=6
        )
        self.description_text.pack(fill=tk.X, pady=(0, 15))
    
    def create_form_buttons(self):
        # Form buttons
        self.buttons_frame = tk.Frame(self.form_card, bg=COLORS["bg_card"])
        self.buttons_frame.pack(fill=tk.X, pady=15, padx=15)
        
        # Clear button
        self.clear_button = tk.Button(
            self.buttons_frame,
            text="Clear Form",
            font=("Segoe UI", 11),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            padx=20,
            pady=10,
            bd=0,
            cursor="hand2",
            activebackground=COLORS["border"],
            command=self.clear_form
        )
        self.clear_button.pack(side=tk.LEFT)
        
        # Save button
        self.save_button = tk.Button(
            self.buttons_frame,
            text="Save Item",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["secondary"],
            fg=COLORS["text_light"],
            padx=20,
            pady=10,
            bd=0,
            cursor="hand2",
            activebackground=COLORS["secondary_hover"],
            activeforeground=COLORS["text_light"],
            command=self.save_item
        )
        self.save_button.pack(side=tk.RIGHT)
    
    def choose_image(self):
        # Open file dialog to select image
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
        
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        
        if image_path:
            try:
                # Update image path
                self.image_path = image_path
                
                # Display image preview
                img = Image.open(image_path)
                img = img.resize((200, 200), Image.LANCZOS)
                
                # Clear previous content
                for widget in self.image_preview_frame.winfo_children():
                    widget.destroy()
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                self.image_preview = photo  # Keep reference
                
                # Display in preview frame
                img_label = tk.Label(
                    self.image_preview_frame,
                    image=photo,
                    bg=COLORS["border"]
                )
                img_label.pack(fill=tk.BOTH, expand=True)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
    
    def clear_form(self):
        # Clear all form fields
        self.name_entry.delete(0, tk.END)
        self.category_combobox.current(0)
        self.price_entry.delete(0, tk.END)
        self.old_price_entry.delete(0, tk.END)
        self.stock_var.set(True)
        self.description_text.delete("1.0", tk.END)
        
        # Clear image preview
        self.image_path = None
        for widget in self.image_preview_frame.winfo_children():
            widget.destroy()
        
        self.preview_label = tk.Label(
            self.image_preview_frame,
            text="No Image Selected",
            font=("Segoe UI", 11),
            bg=COLORS["border"],
            fg=COLORS["text_secondary"]
        )
        self.preview_label.pack(expand=True)
    
    def validate_form(self):
        # Get values
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        
        # Validate required fields
        if not name:
            messagebox.showerror("Validation Error", "Item name is required")
            return False
        
        if not price:
            messagebox.showerror("Validation Error", "Price is required")
            return False
        
        # Validate price is a number
        try:
            float(price)
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a valid number")
            return False
        
        # Validate old price if provided
        old_price = self.old_price_entry.get().strip()
        if old_price:
            try:
                float(old_price)
            except ValueError:
                messagebox.showerror("Validation Error", "Old price must be a valid number")
                return False
        
        return True
    
    def save_item(self):
        if not self.validate_form():
            return
        
        # Get form values
        name = self.name_entry.get().strip()
        category = self.category_combobox.get()
        price = float(self.price_entry.get().strip())
        old_price_str = self.old_price_entry.get().strip()
        old_price = float(old_price_str) if old_price_str else None
        in_stock = self.stock_var.get()
        description = self.description_text.get("1.0", tk.END).strip()
        
        # Generate a simplified name for the image file
        image_name = None
        if self.image_path:
            # Get file extension
            _, ext = os.path.splitext(self.image_path)
            
            # Create a sanitized filename based on item name
            sanitized_name = ''.join(c for c in name.lower() if c.isalnum() or c == ' ')
            sanitized_name = sanitized_name.replace(' ', '_')
            image_name = f"{sanitized_name}{ext}"
            
            # Get absolute path to assets directory
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            os.makedirs(assets_dir, exist_ok=True)
            
            # Copy and resize the image
            try:
                # Open and resize image
                img = Image.open(self.image_path)
                img = img.resize((120, 120), Image.LANCZOS)
                
                # Save to assets folder
                image_path = os.path.join(assets_dir, image_name)
                img.save(image_path)
                
                # Print success message for debugging
                print(f"Image saved successfully to: {image_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
                return
        
        # Create item data
        item_data = {
            "id": 0,  # This would be updated with real ID in a database scenario
            "name": name,
            "category": category,
            "price": price,
            "in_stock": in_stock,
            "image_name": image_name,
            "description": description
        }
        
        if old_price:
            item_data["old_price"] = old_price
        
        # Call callback if provided
        if self.on_item_added:
            self.on_item_added(item_data)
        
        # Show success message
        messagebox.showinfo("Success", f"Item '{name}' has been added successfully")
        
        # Clear the form
        self.clear_form()
