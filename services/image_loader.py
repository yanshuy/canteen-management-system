import os
from PIL import Image
import customtkinter

class ImageLoader:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.getcwd()
        self.cache = {}
        
    def load_image(self, image_path, size=(100, 100)):
        """
        Load an image from the given path and convert it to a CTkImage.
        Caches images to avoid reloading them.
        """
        # Check if image is already in cache
        cache_key = f"{image_path}_{size[0]}x{size[1]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Construct absolute path if needed
        if not os.path.isabs(image_path):
            image_path = os.path.join(self.base_dir, image_path)
        
        try:
            # Try to load the image
            if os.path.exists(image_path):
                pil_image = Image.open(image_path)
                ctk_image = customtkinter.CTkImage(pil_image, size=size)
                # Cache the image
                self.cache[cache_key] = ctk_image
                return ctk_image
            else:
                # Return a placeholder image if not found
                return self._get_placeholder(size)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return self._get_placeholder(size)
    
    def _get_placeholder(self, size=(100, 100)):
        """Create a placeholder image for when an image can't be loaded."""
        cache_key = f"placeholder_{size[0]}x{size[1]}"
        
        if cache_key not in self.cache:
            pil_image = Image.new("RGB", size, "gray")
            self.cache[cache_key] = customtkinter.CTkImage(pil_image, size=size)
            
        return self.cache[cache_key]
