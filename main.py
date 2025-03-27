import customtkinter
import os

from services import MenuService, CartService, ImageLoader
from gui import MenuView, CartView

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
        
        # Initialize services
        self.menu_service = MenuService()
        self.cart_service = CartService()
        self.image_loader = ImageLoader(base_dir=self.base_dir)
        
        # Create view container frame 
        self.container_frame = customtkinter.CTkFrame(self.app)
        self.container_frame.pack(fill="both", expand=True)
        
        # Start with menu view
        self.show_menu_view()
    
    def clear_container(self):
        """Clear the container frame for view switching"""
        for widget in self.container_frame.winfo_children():
            widget.destroy()
    
    def show_menu_view(self):
        """Switch to menu view"""
        self.clear_container()
        self.menu_view = MenuView(
            self.container_frame, 
            self.menu_service, 
            self.cart_service, 
            self.image_loader,
            on_view_cart=self.show_cart_view  # Pass the callback for Cart button
        )
    
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