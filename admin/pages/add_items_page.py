import customtkinter as ctk
import os
import shutil
from PIL import Image, ImageTk
from utils.colors import COLORS
from utils.widgets import Card
import requests
from tkinter import messagebox

class AddItemsPage(ctk.CTkFrame):
    def __init__(self, parent, on_item_added=None):
        super().__init__(parent)
        self.on_item_added = on_item_added
        self.image_path = None
        self.image_preview = None
        self.configure(fg_color=COLORS["bg_main"])
        self.header = ctk.CTkLabel(self, text="Add New Item", font=ctk.CTkFont(size=28, weight="bold"), text_color=COLORS["text_primary"])
        self.header.pack(pady=(24, 12))
        self.form_card = ctk.CTkFrame(self, corner_radius=18, fg_color=COLORS["bg_card"])
        self.form_card.pack(padx=40, pady=16, fill="both", expand=True)
        self.form_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=24, pady=24)
        self.left_column = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.left_column.pack(side="left", fill="both", expand=True, padx=(0, 24))
        self.right_column = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.right_column.pack(side="right", fill="both", expand=True)
        self.create_left_column()
        self.create_right_column()
        self.create_form_buttons()

    def create_left_column(self):
        label_font = ctk.CTkFont(size=15, weight="bold")
        entry_font = ctk.CTkFont(size=14)
        entry_fg = COLORS["bg_card"]
        entry_text = COLORS["text_primary"]
        border = COLORS["primary"]
        self.name_label = ctk.CTkLabel(self.left_column, text="Item Name:", font=label_font, text_color=COLORS["text_primary"])
        self.name_label.pack(anchor="w", pady=(0, 6))
        self.name_entry = ctk.CTkEntry(self.left_column, font=entry_font, fg_color=entry_fg, border_color=border, border_width=2, text_color=entry_text, height=44, corner_radius=10)
        self.name_entry.pack(fill="x", pady=(0, 18))
        self.category_label = ctk.CTkLabel(self.left_column, text="Category:", font=label_font, text_color=COLORS["text_primary"])
        self.category_label.pack(anchor="w", pady=(0, 6))
        categories = ["Breakfast", "Lunch", "Veg", "Non Veg", "Jain", "North Indian", "South Indian", "Chinese", "Drinks", "Dessert"]
        import tkinter as tk
        self.category_listbox = tk.Listbox(self.left_column, selectmode="multiple", exportselection=0, height=8, font=("Arial", 12))
        for cat in categories:
            self.category_listbox.insert(tk.END, cat)
        self.category_listbox.pack(fill="x", pady=(0, 18))
        # Bind selection event for exclusive Veg/Non Veg/Jain logic
        self.category_listbox.bind('<<ListboxSelect>>', self._exclusive_foodtype_selection)
        self.price_label = ctk.CTkLabel(self.left_column, text="Price:", font=label_font, text_color=COLORS["text_primary"])
        self.price_label.pack(anchor="w", pady=(0, 6))
        self.price_entry = ctk.CTkEntry(self.left_column, font=entry_font, fg_color=entry_fg, border_color=border, border_width=2, text_color=entry_text, height=44, corner_radius=10)
        self.price_entry.pack(fill="x", pady=(0, 18))
        self.old_price_label = ctk.CTkLabel(self.left_column, text="Old Price (Optional):", font=label_font, text_color=COLORS["text_primary"])
        self.old_price_label.pack(anchor="w", pady=(0, 6))
        self.old_price_entry = ctk.CTkEntry(self.left_column, font=entry_font, fg_color=entry_fg, border_color=border, border_width=2, text_color=entry_text, height=44, corner_radius=10)
        self.old_price_entry.pack(fill="x", pady=(0, 18))

    def _exclusive_foodtype_selection(self, event=None):
        # Only one of Veg, Non Veg, Jain can be selected at a time, allow toggling
        food_types = {"Veg", "Non Veg", "Jain"}
        selected_indices = self.category_listbox.curselection()
        # Find indices of food type selections
        foodtype_indices = [i for i in selected_indices if self.category_listbox.get(i) in food_types]
        if len(foodtype_indices) > 1:
            # Deselect all food types except the last selected
            last_selected = foodtype_indices[-1]
            for i in foodtype_indices:
                if i != last_selected:
                    self.category_listbox.selection_clear(i)
        # If user deselects all, do nothing (allows toggling off)

    def create_right_column(self):
        label_font = ctk.CTkFont(size=15, weight="bold")
        entry_font = ctk.CTkFont(size=14)
        entry_fg = COLORS["bg_card"]
        entry_text = COLORS["text_primary"]
        border = COLORS["primary"]
        self.image_label = ctk.CTkLabel(self.right_column, text="Item Image:", font=label_font, text_color=COLORS["text_primary"])
        self.image_label.pack(anchor="w", pady=(0, 6))
        self.image_preview_frame = ctk.CTkFrame(self.right_column, fg_color=COLORS["bg_main"], width=200, height=200, corner_radius=14)
        self.image_preview_frame.pack(pady=(0, 18))
        self.image_preview_frame.pack_propagate(False)
        self.preview_label = ctk.CTkLabel(self.image_preview_frame, text="No Image Selected", font=ctk.CTkFont(size=13), text_color=COLORS["text_secondary"])
        self.preview_label.pack(expand=True)
        self.upload_button = ctk.CTkButton(self.right_column, text="Choose Image", font=entry_font, fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], text_color="white", command=self.choose_image, corner_radius=10, height=44)
        self.upload_button.pack(fill="x", pady=(0, 18))
        self.description_label = ctk.CTkLabel(self.right_column, text="Description (Optional):", font=label_font, text_color=COLORS["text_primary"])
        self.description_label.pack(anchor="w", pady=(0, 6))
        self.description_text = ctk.CTkTextbox(self.right_column, font=entry_font, fg_color=entry_fg, border_color=border, border_width=2, text_color=entry_text, height=90, corner_radius=10)
        self.description_text.pack(fill="x", pady=(0, 18))

    def create_form_buttons(self):
        self.buttons_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=12, padx=12)
        self.clear_button = ctk.CTkButton(self.buttons_frame, text="Clear Form", font=ctk.CTkFont(size=14), fg_color=COLORS["danger"], text_color="white", hover_color=COLORS["danger_hover"], command=self.clear_form, corner_radius=10, height=44)
        self.clear_button.pack(side="left", padx=(0, 12), fill="x", expand=True)
        self.save_button = ctk.CTkButton(self.buttons_frame, text="Save Item", font=ctk.CTkFont(size=14, weight="bold"), fg_color=COLORS["primary"], hover_color=COLORS["secondary"], text_color="white", command=self.save_item, corner_radius=10, height=44)
        self.save_button.pack(side="right", fill="x", expand=True)

    def choose_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
        image_path = ctk.filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        if image_path:
            try:
                self.image_path = image_path
                img = Image.open(image_path)
                img = img.resize((180, 180), Image.LANCZOS)
                for widget in self.image_preview_frame.winfo_children():
                    widget.destroy()
                photo = ImageTk.PhotoImage(img)
                self.image_preview = photo
                img_label = ctk.CTkLabel(
                    self.image_preview_frame,
                    image=photo
                )
                img_label.pack(fill="both", expand=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def clear_form(self):
        self.name_entry.delete(0, ctk.END)
        # Clear all selections in the category listbox
        self.category_listbox.selection_clear(0, 'end')
        self.price_entry.delete(0, ctk.END)
        self.old_price_entry.delete(0, ctk.END)
        self.description_text.delete("1.0", ctk.END)
        self.image_path = None
        for widget in self.image_preview_frame.winfo_children():
            widget.destroy()
        self.preview_label = ctk.CTkLabel(
            self.image_preview_frame,
            text="No Image Selected",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        )
        self.preview_label.pack(expand=True)

    def validate_form(self):
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Item name is required")
            return False
        if not price:
            messagebox.showerror("Validation Error", "Price is required")
            return False
        try:
            float(price)
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a valid number")
            return False
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
        name = self.name_entry.get().strip()
        # Get all selected categories and join with commas
        selected_indices = self.category_listbox.curselection()
        selected_categories = [self.category_listbox.get(i) for i in selected_indices]
        category = ",".join(selected_categories)
        price = self.price_entry.get().strip()
        old_price_str = self.old_price_entry.get().strip()
        old_price = f"₹{old_price_str}" if old_price_str else None
        description = self.description_text.get("1.0", ctk.END).strip()
        image_name = None
        if self.image_path:
            _, ext = os.path.splitext(self.image_path)
            sanitized_name = ''.join(c for c in name.lower() if c.isalnum() or c == ' ')
            sanitized_name = sanitized_name.replace(' ', '_')
            image_name = f"{sanitized_name}{ext}"
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            os.makedirs(assets_dir, exist_ok=True)
            try:
                img = Image.open(self.image_path)
                img = img.resize((120, 120), Image.LANCZOS)
                image_path = os.path.join(assets_dir, image_name)
                img.save(image_path)
                print(f"Image saved successfully to: {image_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
                return
        item_data = {
            "id": 0,
            "name": name,
            "category": category,
            "price": f"₹{price}",
            "image_name": image_name,
            "description": description
        }
        if old_price:
            item_data["old_price"] = old_price
        backend_item_data = {
            "name": name,
            "price": f"₹{price}",
            "description": description,
            "image_url": image_name if image_name else "",
            "category": category
        }
        try:
            response = requests.post(
                "http://127.0.0.1:5000/menu-items",
                json=backend_item_data,
                timeout=5
            )
            if response.status_code == 201:
                messagebox.showinfo("Success", f"Item '{name}' has been added to the database.")
            else:
                messagebox.showerror("Error", f"Failed to add item to database: {response.json().get('message', 'Unknown error')}")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to backend: {e}")
            return
        self.clear_form()
