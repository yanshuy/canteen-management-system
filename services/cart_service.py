class CartService:
    def __init__(self):
        self.cart_items = {}  # Dictionary to store item_name: quantity
        self.listeners = []   # List of callback functions to notify on cart changes
        self.next_listener_id = 0  # For tracking listeners to enable removal
    
    def add_item(self, item_name, quantity=1):
        """Add an item to the cart"""
        current_qty = self.cart_items.get(item_name, 0)
        self.cart_items[item_name] = current_qty + quantity
        self._notify_listeners()
    
    def update_quantity(self, item_name, quantity):
        """Update the quantity of an item in the cart"""
        if quantity <= 0:
            if item_name in self.cart_items:
                del self.cart_items[item_name]
        else:
            self.cart_items[item_name] = quantity
        self._notify_listeners()
    
    def get_quantity(self, item_name):
        """Get the quantity of an item in the cart"""
        return self.cart_items.get(item_name, 0)
    
    def get_total_items(self):
        """Get the total number of items in the cart"""
        return sum(self.cart_items.values())
    
    def get_all_items(self):
        """Get all items in the cart"""
        return self.cart_items
    
    def clear_cart(self):
        """Clear all items from the cart"""
        self.cart_items = {}
        self._notify_listeners()
    
    def add_listener(self, callback):
        """Add a listener to be notified when the cart changes"""
        listener_id = self.next_listener_id
        self.next_listener_id += 1
        self.listeners.append((listener_id, callback))
        return listener_id
    
    def remove_listener(self, listener_id):
        """Remove a listener by its ID"""
        self.listeners = [(lid, callback) for lid, callback in self.listeners if lid != listener_id]
    
    def _notify_listeners(self):
        """Notify all listeners that the cart has changed"""
        # Create a copy of listeners to avoid issues if a listener gets removed during notification
        listeners_copy = self.listeners.copy()
        
        for lid, callback in listeners_copy:
            try:
                # Only notify if the listener still exists
                if lid in [l[0] for l in self.listeners]:
                    callback(self.cart_items)
            except Exception as e:
                print(f"Error notifying listener {lid}: {e}")
                # Don't remove the listener automatically - could be a temporary error
