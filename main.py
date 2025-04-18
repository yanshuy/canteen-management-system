import customtkinter
import os

from services import MenuService, CartService, ImageCache, AuthService
from gui import MenuView, CartView
from gui.login import LoginView

class CanteenApp:
    def __init__(self):
        # Set appearance settings
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        
        # Create main window
        self.app = customtkinter.CTk()
        self.app.geometry("720x920")
        self.app.title("canteen management system")
        
        # Get the base directory for the project
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ensure the cache directory exists
        cache_dir = os.path.join(self.base_dir, "static", "cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize services
        self.menu_service = MenuService()
        self.cart_service = CartService()
        self.image_cache = ImageCache()  # Initialize global image cache
        self.auth_service = AuthService()  # Add AuthService
        
        # Create view container frame 
        self.container_frame = customtkinter.CTkFrame(self.app)
        self.container_frame.pack(fill="both", expand=True)
        
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start with login view
        self.show_login_view()
    
    def clear_container(self):
        """Clear the container frame for view switching"""
        for widget in self.container_frame.winfo_children():
            widget.destroy()
    
    def preload_menu_images(self):
        """Preload all menu item images in the background while user is logging in."""
        items = self.menu_service.get_all_items()
        for item in items:
            url = item.get("image_url")
            if url:
                # Preload with default menu image size (used in MenuView)
                self.image_cache.get_image(url, size=(120, 120))
    
    def show_login_view(self):
        """Switch to login view and start preloading menu images."""
        self.clear_container()
        self.login_view = LoginView(
            self.container_frame,
            self.auth_service,
            on_login_success=self.show_menu_view
        )
        # Start preloading images in the background
        self.preload_menu_images()

    def show_menu_view(self, user=None):
        """Switch to menu view (after login)"""
        self.clear_container()
        self.menu_view = MenuView(
            self.container_frame, 
            self.menu_service, 
            self.cart_service,
            on_view_cart=self.show_cart_view  # Pass the callback for Cart button
        )

    def on_close(self):
        """Handle application close event"""
        # Shut down the image cache background thread
        if hasattr(self, 'image_cache'):
            self.image_cache.shutdown()
        
        # Close the app
        self.app.destroy()
    
    def show_cart_view(self):
        """Switch to cart view"""
        self.clear_container()
        self.cart_view = CartView(
            self.container_frame,
            self.cart_service,
            self.menu_service,
            on_back_to_menu=self.show_menu_view
        )
    
    def run(self):
        """Run the application"""
        self.app.mainloop()

def main():
    app = CanteenApp()
    app.run()

if __name__ == "__main__":
    main()