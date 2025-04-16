import os

class MenuService:
    def __init__(self):
        # Sample menu items
        self.menu_items = [
            {"category": ["Breakfast", "veg"], "name": "Pancakes", "price": "₹50", "description": "Fluffy pancakes with maple syrup", "image_url": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYW5jYWtlc3xlbnwwfHx8fDE3NDMwNjA1MTF8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Lunch", "non-veg"], "name": "Sandwich", "price": "₹35", "description": "Club sandwich with fries", "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYW5kd2ljaHxlbnwwfHx8fDE3NDMwNjA1MTJ8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Drinks", "veg"], "name": "Coffee", "price": "₹10", "description": "Freshly brewed coffee", "image_url": "https://images.unsplash.com/photo-1556742526-795a8eac090e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MXwxfHNlYXJjaHwxfHxDb2ZmZWV8ZW58MHx8fHwxNzQzMDYwNTEyfDA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Chinese", "veg"], "name": "Fried Rice", "price": "₹60", "description": "Vegetable fried rice", "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxGcmllZCUyMFJpY2V8ZW58MHx8fHwxNzQzMDYwNTEzfDA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Dessert", "veg"], "name": "Cake", "price": "₹40", "description": "Chocolate cake slice", "image_url": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxDYWtlfGVufDB8fHx8MTc0MzA2MDUxM3ww&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Other", "veg"], "name": "Salad", "price": "₹20", "description": "Greek salad", "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYWxhZHxlbnwwfHx8fDE3NDMwNjA1MTR8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Breakfast", "non-veg"], "name": "Omelette", "price": "₹20", "description": "Three-egg omelette with toast", "image_url": "https://images.unsplash.com/photo-1494597706938-de2cd7341979?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxPbWVsZXR0ZXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Lunch", "non-veg"], "name": "Pasta", "price": "₹50", "description": "Spaghetti carbonara", "image_url": "https://images.unsplash.com/photo-1556761223-4c4282c73f77?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYXN0YXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Drinks", "veg"], "name": "Smoothie", "price": "₹20", "description": "Mixed berry smoothie", "image_url": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTbW9vdGhpZXxlbnwwfHx8fDE3NDMwNjA1MTZ8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": ["Chinese", "Lunch", "jain"], "name": "Chilli Paneer", "price": "₹70", "description": "Spicy paneer with bell peppers", "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1080&q=80"},
            {"category": ["Breakfast", "jain"], "name": "Jain Poha", "price": "₹30", "description": "Poha prepared Jain style without onions and potatoes", "image_url": "https://images.unsplash.com/photo-1567337710282-00832b415979?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1080&q=80"}
        ]
        self.categories = ["All", "Chinese", "Breakfast", "Lunch", "Drinks", "Dessert", "Other", "veg", "non-veg", "jain"]

    def get_all_items(self):
        return self.menu_items

    def get_categories(self):
        return self.categories
        
    def get_food_types(self):
        return ["veg", "non-veg", "jain"]

    def get_items_by_category(self, category):
        if category == "All":
            return self.menu_items
        return [item for item in self.menu_items if category in item["category"]]
        
    def get_items_by_food_type(self, food_type):
        if food_type == "All":
            return self.menu_items
        return [item for item in self.menu_items if food_type in item["category"]]
        
    def get_items_by_category_and_food_type(self, category, food_type):
        if category == "All" and food_type == "All":
            return self.menu_items
        elif category == "All":
            return self.get_items_by_food_type(food_type)
        elif food_type == "All":
            return self.get_items_by_category(category)
        return [item for item in self.menu_items if category in item["category"] and food_type in item["category"]]
