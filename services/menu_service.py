import os
import sqlite3

class MenuService:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "canteen.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        self.menu_items = self._load_menu_items_from_db()
        self.categories = self._extract_categories()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                category TEXT
            )
        ''')
        conn.commit()
        # Check if table is empty, then populate with initial data
        c.execute('SELECT COUNT(*) FROM menu_items')
        if c.fetchone()[0] == 0:
            initial_items = [
                ("Pancakes", "₹50", "Fluffy pancakes with maple syrup", "https://images.unsplash.com/photo-1528207776546-365bb710ee93?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYW5jYWtlc3xlbnwwfHx8fDE3NDMwNjA1MTF8MA&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,veg"),
                ("Sandwich", "₹35", "Club sandwich with fries", "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYW5kd2ljaHxlbnwwfHx8fDE3NDMwNjA1MTJ8MA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,non-veg"),
                ("Coffee", "₹10", "Freshly brewed coffee", "https://images.unsplash.com/photo-1556742526-795a8eac090e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MXwxfHNlYXJjaHwxfHxDb2ZmZWV8ZW58MHx8fHwxNzQzMDYwNTEyfDA&ixlib=rb-4.0.3&q=80&w=1080", "Drinks,veg"),
                ("Fried Rice", "₹60", "Vegetable fried rice", "https://images.unsplash.com/photo-1512058564366-18510be2db19?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxGcmllZCUyMFJpY2V8ZW58MHx8fHwxNzQzMDYwNTEzfDA&ixlib=rb-4.0.3&q=80&w=1080", "Chinese,veg"),
                ("Cake", "₹40", "Chocolate cake slice", "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxDYWtlfGVufDB8fHx8MTc0MzA2MDUxM3ww&ixlib=rb-4.0.3&q=80&w=1080", "Dessert,veg"),
                ("Salad", "₹20", "Greek salad", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYWxhZHxlbnwwfHx8fDE3NDMwNjA1MTR8MA&ixlib=rb-4.0.3&q=80&w=1080", "Other,veg"),
                ("Omelette", "₹20", "Three-egg omelette with toast", "https://images.unsplash.com/photo-1494597706938-de2cd7341979?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxPbWVsZXR0ZXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,non-veg"),
                ("Pasta", "₹50", "Spaghetti carbonara", "https://images.unsplash.com/photo-1556761223-4c4282c73f77?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYXN0YXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,non-veg"),
                ("Smoothie", "₹20", "Mixed berry smoothie", "https://images.unsplash.com/photo-1505252585461-04db1eb84625?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTbW9vdGhpZXxlbnwwfHx8fDE3NDMwNjA1MTZ8MA&ixlib=rb-4.0.3&q=80&w=1080", "Drinks,veg"),
                ("Chilli Paneer", "₹70", "Spicy paneer with bell peppers", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1080&q=80", "Chinese,Lunch,jain"),
                ("Jain Poha", "₹30", "Poha prepared Jain style without onions and potatoes", "https://images.unsplash.com/photo-1567337710282-00832b415979?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1080&q=80", "Breakfast,jain")
            ]
            c.executemany('''
                INSERT INTO menu_items (name, price, description, image_url, category)
                VALUES (?, ?, ?, ?, ?)
            ''', initial_items)
            conn.commit()
        conn.close()

    def _load_menu_items_from_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT name, price, description, image_url, category FROM menu_items')
        rows = c.fetchall()
        conn.close()
        items = []
        for row in rows:
            name, price, description, image_url, category = row
            categories = [cat.strip() for cat in category.split(",") if cat.strip()]
            items.append({
                "name": name,
                "price": price,
                "description": description,
                "image_url": image_url,
                "category": categories
            })
        return items

    def _extract_categories(self):
        cats = set()
        for item in self.menu_items:
            for cat in item["category"]:
                cats.add(cat)
        return ["All"] + sorted(cats)

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
