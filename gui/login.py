import tkinter
import customtkinter
from PIL import Image
import os

class LoginView:
    def __init__(self, root, auth_service, on_login_success=None):
        self.root = root
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        
        # Define color scheme - matching the one from MenuView
        self.colors = {
            "primary": "#4D77FF",
            "secondary": "#5C77E6",
            "accent": "#FF8C32",
            "success": "#38B000",
            "error": "#FF3333",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "card_bg": ("#FFFFFF", "#2B2B2B"),
            "hover": ("#E6E6E6", "#3A3A3A"),
            "border": ("#E0E0E0", "#3A3A3A")
        }
        
        # Load and use the actual logo image from the root folder
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png")
        if os.path.exists(logo_path):
            self.logo_image = customtkinter.CTkImage(
                Image.open(logo_path).resize((100, 100)),
                size=(100, 100)
            )
        else:
            self.logo_image = customtkinter.CTkImage(
                Image.new("RGB", (100, 100), "gray"),
                size=(100, 100)
            )
        
        self._create_ui()
    
    def _create_ui(self):
        # Center the login card in the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container for login
        self.login_frame = customtkinter.CTkFrame(
            self.root,
            corner_radius=12,
            fg_color=self.colors["card_bg"],
            border_width=1,
            border_color=self.colors["border"],
            width=400,
            height=500
        )
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.login_frame.grid_propagate(False)
        
        # Center content in the frame
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=0)
        self.login_frame.grid_columnconfigure(0, weight=1)
        
        # Logo and app title
        logo_label = customtkinter.CTkLabel(
            self.login_frame,
            text="",
            image=self.logo_image
        )
        logo_label.grid(row=0, column=0, pady=(50, 10))
        
        title_label = customtkinter.CTkLabel(
            self.login_frame,
            text="🍴 Canteeny",
            font=customtkinter.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=1, column=0, pady=(0, 30))
        
        # Welcome message
        welcome_label = customtkinter.CTkLabel(
            self.login_frame,
            text="Welcome back!",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        welcome_label.grid(row=2, column=0, pady=(0, 30))
        
        # Username field
        self.username_entry = customtkinter.CTkEntry(
            self.login_frame,
            placeholder_text="Username or Email",
            width=300,
            height=45,
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
            font=customtkinter.CTkFont(size=14)
        )
        self.username_entry.grid(row=4, column=0, padx=50, pady=(0, 15))
        
        # Password field
        self.password_entry = customtkinter.CTkEntry(
            self.login_frame,
            placeholder_text="Password",
            width=300,
            height=45,
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
            show="•",
            font=customtkinter.CTkFont(size=14)
        )
        self.password_entry.grid(row=5, column=0, padx=50, pady=(0, 10))
        
        # Error message label (hidden by default)
        self.error_label = customtkinter.CTkLabel(
            self.login_frame,
            text="",
            text_color=self.colors["error"],
            font=customtkinter.CTkFont(size=13)
        )
        self.error_label.grid(row=6, column=0, pady=(0, 15))
        self.error_label.grid_remove()  # Hide initially
        
        # Login button
        login_button = customtkinter.CTkButton(
            self.login_frame,
            text="Login",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            corner_radius=8,
            command=self.login,
            width=300,
            height=45
        )
        login_button.grid(row=8, column=0, padx=50, pady=(20, 10))

        # Register button
        register_button = customtkinter.CTkButton(
            self.login_frame,
            text="Register",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["secondary"],
            corner_radius=8,
            command=self.open_register_window,
            width=300,
            height=45
        )
        register_button.grid(row=9, column=0, padx=50, pady=(0, 20))
        
    def show_error(self, message):
        """Show error message below password field"""
        self.error_label.configure(text=message)
        self.error_label.grid()
        
    def hide_error(self):
        """Hide error message"""
        self.error_label.grid_remove()
        
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Attempt login
        try:
            # Call the authentication service
            login_result = self.auth_service.login(username, password)
            
            if login_result.get("success"):
                # Hide the error if it was previously shown
                self.hide_error()
                
                # Call success callback
                if self.on_login_success:
                    self.on_login_success(login_result.get("user"))
            else:
                # Show error message
                self.show_error(login_result.get("message", "Login failed. Please try again."))
                
        except Exception as e:
            self.show_error(f"An error occurred: {str(e)}")
            
    def forgot_password(self):
        """Handle forgot password click"""
        # Implementation would depend on your app's flow
        print("Forgot password clicked")
        # This would typically open a password reset screen
        
    def show_signup(self):
        """Handle sign up link click"""
        # Implementation would depend on your app's flow
        print("Sign up clicked")
        # This would typically switch to a signup screen

    def open_register_window(self):
        RegisterWindow(self.root, self.auth_service, self.colors)

class RegisterWindow:
    def __init__(self, parent, auth_service, colors):
        self.auth_service = auth_service
        self.colors = colors
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title("Register")
        # Set the registration window to cover the full screen (Windows compatible)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.grab_set()
        self._create_ui()

    def _create_ui(self):
        # Centered frame for registration form
        form_frame = customtkinter.CTkFrame(
            self.window,
            corner_radius=12,
            fg_color=self.colors["card_bg"],
            border_width=1,
            border_color=self.colors["border"],
            width=420,
            height=480
        )
        form_frame.place(relx=0.5, rely=0.5, anchor="c")
        form_frame.pack_propagate(False)

        title = customtkinter.CTkLabel(
            form_frame,
            text="Create Account",
            font=customtkinter.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(30, 20))

        self.fullname_entry = customtkinter.CTkEntry(
            form_frame,
            placeholder_text="Full Name",
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
            font=customtkinter.CTkFont(size=14)
        )
        self.fullname_entry.pack(pady=(0, 12))

        self.username_entry = customtkinter.CTkEntry(
            form_frame,
            placeholder_text="Username",
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
            font=customtkinter.CTkFont(size=14)
        )
        self.username_entry.pack(pady=(0, 12))

        self.password_entry = customtkinter.CTkEntry(
            form_frame,
            placeholder_text="Password",
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
            show="•",
            font=customtkinter.CTkFont(size=14)
        )
        self.password_entry.pack(pady=(0, 12))

        self.confirm_password_entry = customtkinter.CTkEntry(
            form_frame,
            placeholder_text="Confirm Password",
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border"],
            show="•",
            font=customtkinter.CTkFont(size=14)
        )
        self.confirm_password_entry.pack(pady=(0, 12))

        self.error_label = customtkinter.CTkLabel(
            form_frame,
            text="",
            text_color=self.colors["error"],
            font=customtkinter.CTkFont(size=13)
        )
        self.error_label.pack(pady=(0, 10))

        register_btn = customtkinter.CTkButton(
            form_frame,
            text="Register",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            corner_radius=8,
            command=self.register,
            width=300,
            height=40
        )
        register_btn.pack(pady=(10, 10))

    def register(self):
        full_name = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        if not full_name or not username or not password or not confirm_password:
            self.error_label.configure(text="All fields are required")
            return
        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match")
            return
        result = self.auth_service.register(username, password, full_name)
        if result.get("success"):
            self.error_label.configure(text="Registered successfully!", text_color=self.colors["success"])
            self.window.after(1200, self.window.destroy)
        else:
            self.error_label.configure(text=result.get("message", "Registration failed"), text_color=self.colors["error"])

