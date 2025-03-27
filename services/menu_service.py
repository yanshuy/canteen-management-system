import os

class MenuService:
    def __init__(self):
        # Sample menu items
        self.menu_items = [
            {"category": "Breakfast", "name": "Pancakes", "price": "₹50", "description": "Fluffy pancakes with maple syrup", "image_url": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYW5jYWtlc3xlbnwwfHx8fDE3NDMwNjA1MTF8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Lunch", "name": "Sandwich", "price": "₹35", "description": "Club sandwich with fries", "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYW5kd2ljaHxlbnwwfHx8fDE3NDMwNjA1MTJ8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Drinks", "name": "Coffee", "price": "₹10", "description": "Freshly brewed coffee", "image_url": "https://images.unsplash.com/photo-1556742526-795a8eac090e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MXwxfHNlYXJjaHwxfHxDb2ZmZWV8ZW58MHx8fHwxNzQzMDYwNTEyfDA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Chinese", "name": "Fried Rice", "price": "₹60", "description": "Vegetable fried rice", "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxGcmllZCUyMFJpY2V8ZW58MHx8fHwxNzQzMDYwNTEzfDA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Dessert", "name": "Cake", "price": "₹40", "description": "Chocolate cake slice", "image_url": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxDYWtlfGVufDB8fHx8MTc0MzA2MDUxM3ww&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Other", "name": "Salad", "price": "₹20", "description": "Greek salad", "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYWxhZHxlbnwwfHx8fDE3NDMwNjA1MTR8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Breakfast", "name": "Omelette", "price": "₹20", "description": "Three-egg omelette with toast", "image_url": "https://images.unsplash.com/photo-1494597706938-de2cd7341979?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxPbWVsZXR0ZXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Lunch", "name": "Pasta", "price": "₹50", "description": "Spaghetti carbonara", "image_url": "https://images.unsplash.com/photo-1556761223-4c4282c73f77?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYXN0YXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080"},
            {"category": "Drinks", "name": "Smoothie", "price": "₹20", "description": "Mixed berry smoothie", "image_url": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTbW9vdGhpZXxlbnwwfHx8fDE3NDMwNjA1MTZ8MA&ixlib=rb-4.0.3&q=80&w=1080"},
        ]
        self.categories = ["All", "Chinese", "Breakfast", "Lunch", "Drinks", "Dessert", "Other"]
        

    def get_all_items(self):
        return self.menu_items

    def get_categories(self):
        return self.categories

    def get_items_by_category(self, category):
        if category == "All":
            return self.menu_items
        return [item for item in self.menu_items if item["category"] == category]
