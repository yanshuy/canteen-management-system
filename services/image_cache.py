import requests
from PIL import Image
from io import BytesIO
import customtkinter
import threading
import time
import os
from pathlib import Path

class ImageCache:
    """
    Singleton image cache service that manages both memory and disk caching
    of images to improve performance.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageCache, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.memory_cache = {}  # In-memory cache for faster access
        self.disk_cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                         "static", "cache")
        self.background_queue = []  # Queue for background loading
        self.is_running = False
        self.lock = threading.Lock()
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.disk_cache_dir, exist_ok=True)
        print(f"Image cache directory: {self.disk_cache_dir}")
        
        # Start background loading thread
        self._start_background_loader()
        self._initialized = True
    
    def _start_background_loader(self):
        """Start the background thread for loading images"""
        self.is_running = True
        self.bg_thread = threading.Thread(target=self._background_loader, daemon=True)
        self.bg_thread.start()
    
    def _background_loader(self):
        """Background thread that loads images from queue"""
        while self.is_running:
            try:
                # Check if there are items in the queue
                if self.background_queue:
                    with self.lock:
                        # Get an item from the queue if available
                        if self.background_queue:
                            url, size, callback = self.background_queue.pop(0)
                            # Skip if already in memory cache
                            if self._get_cache_key(url, size) in self.memory_cache:
                                if callback:
                                    callback(self.memory_cache[self._get_cache_key(url, size)])
                                continue
                    
                    # Not in memory cache, try to load
                    try:
                        print(f"Background loading image: {url}")
                        image = self._load_and_cache_image(url, size)
                        if callback and image:
                            print(f"Image loaded, calling callback for {url}")
                            callback(image)
                    except Exception as e:
                        print(f"Error in background loading of {url}: {e}")
                
                # Sleep a bit to avoid consuming too much CPU
                time.sleep(0.01)
            except Exception as e:
                print(f"Error in background loader: {e}")
                time.sleep(0.1)
    
    def _get_cache_key(self, url, size):
        """Generate a unique key for the cache based on URL and size"""
        return f"{url}_{size[0]}x{size[1]}"
    
    def _get_disk_cache_path(self, url, size):
        """Generate a filepath for disk caching"""
        # Create a filename from the URL using a hash to avoid file system issues
        import hashlib
        filename = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.disk_cache_dir, f"{filename}_{size[0]}x{size[1]}.png")
    
    def _load_from_disk_cache(self, url, size):
        """Try to load image from disk cache"""
        cache_path = self._get_disk_cache_path(url, size)
        if os.path.exists(cache_path):
            try:
                pil_image = Image.open(cache_path)
                ctk_image = customtkinter.CTkImage(pil_image, size=size)
                print(f"Loaded from disk cache: {url}")
                return ctk_image
            except Exception as e:
                print(f"Error loading from disk cache: {e}")
        return None
    
    def _save_to_disk_cache(self, url, size, pil_image):
        """Save image to disk cache"""
        try:
            cache_path = self._get_disk_cache_path(url, size)
            pil_image.save(cache_path, format="PNG")
            print(f"Saved to disk cache: {url}")
        except Exception as e:
            print(f"Error saving to disk cache: {e}")
    
    def _load_and_cache_image(self, url, size):
        """Load an image from URL, cache it, and return CTkImage"""
        # Check disk cache first
        ctk_image = self._load_from_disk_cache(url, size)
        if ctk_image:
            self.memory_cache[self._get_cache_key(url, size)] = ctk_image
            return ctk_image
            
        # Not in disk cache, download it
        try:
            # Add a lower-quality parameter to the URL for faster loading if it's from Unsplash
            modified_url = url
            if "unsplash.com" in url and "q=" in url:
                # Reduce quality for faster loading
                modified_url = url.replace("q=80", "q=60").replace("w=1080", "w=600")
                
            print(f"Downloading image: {modified_url}")
            response = requests.get(modified_url, timeout=5)
            if response.status_code != 200:
                print(f"Failed to download image: {response.status_code}")
                return None
                
            pil_image = Image.open(BytesIO(response.content))
            print(f"Downloaded image: {url}, size: {pil_image.size}")
            
            # Optimize image size
            if max(pil_image.size) > max(size) * 2:
                # Resize if the image is much larger than needed
                scale = max(size) * 2 / max(pil_image.size)
                new_size = (int(pil_image.size[0] * scale), int(pil_image.size[1] * scale))
                pil_image = pil_image.resize(new_size, Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
                print(f"Resized image to: {new_size}")
            
            # Convert to CTkImage
            ctk_image = customtkinter.CTkImage(pil_image, size=size)
            
            # Cache in memory
            self.memory_cache[self._get_cache_key(url, size)] = ctk_image
            
            # Save to disk cache in the background
            threading.Thread(target=self._save_to_disk_cache, 
                            args=(url, size, pil_image), 
                            daemon=True).start()
            
            return ctk_image
        except Exception as e:
            print(f"Error loading image from URL {url}: {e}")
            return None
    
    def get_image(self, url, size=(120, 120), callback=None, placeholder=None):
        """
        Get an image from the cache or load it asynchronously.
        Prevents duplicate background loading for the same image and size.
        """
        cache_key = self._get_cache_key(url, size)

        # Check if image is in memory cache
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]

        # Check if image is in disk cache
        disk_cached = self._load_from_disk_cache(url, size)
        if disk_cached:
            self.memory_cache[cache_key] = disk_cached
            return disk_cached

        # Not cached, queue for background loading
        with self.lock:
            # Prevent duplicate queueing for the same image/size/callback
            already_queued = any(item[0] == url and item[1] == size and item[2] == callback for item in self.background_queue)
            if not already_queued:
                print(f"Queuing image for background loading: {url}")
                self.background_queue.append((url, size, callback))

        # Return placeholder while loading
        return placeholder
    
    def clear_memory_cache(self):
        """Clear the in-memory cache to free up memory"""
        self.memory_cache = {}
    
    def clear_disk_cache(self):
        """Clear the disk cache"""
        for file in os.listdir(self.disk_cache_dir):
            if file.endswith('.png'):
                os.remove(os.path.join(self.disk_cache_dir, file))
    
    def shutdown(self):
        """Properly shut down the background thread"""
        self.is_running = False
        if hasattr(self, 'bg_thread') and self.bg_thread.is_alive():
            self.bg_thread.join(timeout=1.0)