import os

class MenuService:
    def __init__(self):
        # Sample menu items
        self.menu_items = [
            {"category": "Breakfast", "name": "Pancakes", "price": "₹50", "description": "Fluffy pancakes with maple syrup", "image_path": "static/images/Pancakes/Pancakes_1.jpg"},
            {"category": "Lunch", "name": "Sandwich", "price": "₹35", "description": "Club sandwich with fries", "image_path": "static/images/Sandwich/Sandwich_1.jpg"},
            {"category": "Drinks", "name": "Coffee", "price": "₹10", "description": "Freshly brewed coffee", "image_path": "static/images/Coffee/Coffee_1.jpg"},
            {"category": "Chinese", "name": "Fried Rice", "price": "₹60", "description": "Vegetable fried rice", "image_path": "static/images/Fried_Rice/Fried_Rice_1.jpg"},
            {"category": "Dessert", "name": "Cake", "price": "₹40", "description": "Chocolate cake slice", "image_path": "static/images/Cake/Cake_1.jpg"},
            {"category": "Other", "name": "Salad", "price": "₹20", "description": "Greek salad", "image_path": "static/images/Salad/Salad_1.jpg"},
            {"category": "Breakfast", "name": "Omelette", "price": "₹20", "description": "Three-egg omelette with toast", "image_path": "static/images/Omelette/Omelette_1.jpg"},
            {"category": "Lunch", "name": "Pasta", "price": "₹50", "description": "Spaghetti carbonara", "image_path": "static/images/Pasta/Pasta_1.jpg"},
            {"category": "Drinks", "name": "Smoothie", "price": "₹20", "description": "Mixed berry smoothie", "image_path": "static/images/Smoothie/Smoothie_1.jpg"},
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
