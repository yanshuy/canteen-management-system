import tkinter as tk
from utils.colors import COLORS

class SidebarButton(tk.Frame):
    def __init__(self, parent, text, command, bg_color=None, hover_color=None):
        super().__init__(parent, bg=COLORS["bg_sidebar"])
        
        self.bg_color = bg_color or COLORS["bg_sidebar"]
        self.hover_color = hover_color or COLORS["sidebar_hover"]
        self.active_color = COLORS["sidebar_active"]
        self.is_active = False
        
        # Create the button
        self.button = tk.Label(
            self,
            text=text,
            bg=self.bg_color,
            fg=COLORS["text_light"],
            font=("Helvetica", 12),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.button.pack(fill=tk.X)
        
        # Bind events
        self.button.bind("<Button-1>", lambda e: command())
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        if not self.is_active:
            self.button.config(bg=self.hover_color)
    
    def on_leave(self, event):
        if not self.is_active:
            self.button.config(bg=self.bg_color)
    
    def set_active(self, active):
        self.is_active = active
        if active:
            self.button.config(bg=self.active_color, font=("Helvetica", 12, "bold"))
        else:
            self.button.config(bg=self.bg_color, font=("Helvetica", 12))

class Card(tk.Frame):
    def __init__(self, parent, title=None, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["bg_card"],
            padx=15,
            pady=15,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            **kwargs
        )
        
        if title:
            self.title_label = tk.Label(
                self,
                text=title,
                font=("Helvetica", 14, "bold"),
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"]
            )
            self.title_label.pack(anchor="w", pady=(0, 10))

