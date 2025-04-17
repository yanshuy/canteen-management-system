import os
import sqlite3

class MenuService:
    def __init__(self):  # Fixed initialization method name
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "canteen.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        self.menu_items = self._load_menu_items_from_db()
        self.categories = self._extract_categories()
        self._listeners = []
        self._next_listener_id = 1

    def add_listener(self, callback):
        """Add a listener to be notified when the menu changes"""
        lid = self._next_listener_id
        self._next_listener_id += 1
        self._listeners.append((lid, callback))
        return lid

    def remove_listener(self, listener_id):
        """Remove a listener by its ID"""
        self._listeners = [(lid, cb) for lid, cb in self._listeners if lid != listener_id]

    def _notify_listeners(self):
        """Notify all listeners that the menu has changed"""
        listeners_copy = self._listeners.copy()
        for lid, callback in listeners_copy:
            try:
                if lid in [l[0] for l in self._listeners]:
                    callback(self.menu_items)
            except Exception as e:
                print(f"Error notifying menu listener {lid}: {e}")

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
                # Original Items
                ("Pancakes", "₹50", "Fluffy pancakes with maple syrup", "https://images.unsplash.com/photo-1528207776546-365bb710ee93?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYW5jYWtlc3xlbnwwfHx8fDE3NDMwNjA1MTF8MA&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,Veg"),
                ("Sandwich", "₹35", "Club sandwich with fries", "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYW5kd2ljaHxlbnwwfHx8fDE3NDMwNjA1MTJ8MA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,Non Veg"),
                ("Coffee", "₹10", "Freshly brewed coffee", "https://images.unsplash.com/photo-1556742526-795a8eac090e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MXwxfHNlYXJjaHwxfHxDb2ZmZWV8ZW58MHx8fHwxNzQzMDYwNTEyfDA&ixlib=rb-4.0.3&q=80&w=1080", "Drinks,Veg"),
                ("Fried Rice", "₹60", "Vegetable fried rice", "https://images.unsplash.com/photo-1512058564366-18510be2db19?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxGcmllZCUyMFJpY2V8ZW58MHx8fHwxNzQzMDYwNTEzfDA&ixlib=rb-4.0.3&q=80&w=1080", "Chinese,Veg"),
                ("Cake", "₹40", "Chocolate cake slice", "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxDYWtlfGVufDB8fHx8MTc0MzA2MDUxM3ww&ixlib=rb-4.0.3&q=80&w=1080", "Dessert,Veg"),
                ("Salad", "₹20", "Greek salad", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYWxhZHxlbnwwfHx8fDE3NDMwNjA1MTR8MA&ixlib=rb-4.0.3&q=80&w=1080", "Other,Veg"),
                ("Omelette", "₹20", "Three-egg omelette with toast", "https://images.unsplash.com/photo-1494597706938-de2cd7341979?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxPbWVsZXR0ZXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,Non Veg"),
                ("Pasta", "₹50", "Spaghetti carbonara", "https://images.unsplash.com/photo-1556761223-4c4282c73f77?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYXN0YXxlbnwwfHx8fDE3NDMwNjA1MTV8MA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,Non Veg"),
                ("Smoothie", "₹20", "Mixed berry smoothie", "https://images.unsplash.com/photo-1505252585461-04db1eb84625?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTbW9vdGhpZXxlbnwwfHx8fDE3NDMwNjA1MTZ8MA&ixlib=rb-4.0.3&q=80&w=1080", "Drinks,Veg"),
                ("Chilli Paneer", "₹70", "Spicy paneer with bell peppers", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?ixlib=rb-4.0.3&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxDaGlsbGklMjBQYW5lZXJ8ZW58MHx8fHwxNzQ0ODczMDE0fDA&ixlib=rb-4.0.3&q=80&w=1080", "Chinese,Lunch,Jain"),
                ("Jain Poha", "₹30", "Poha prepared Jain style without onions and potatoes", "https://images.unsplash.com/photo-1567337710282-00832b415979?ixlib=rb-4.0.3&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxKYWluJTIwUG9oYXxlbnwwfHx8fDE3NDQ4NzMwMTd8MA&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,Jain"),
                
                # Additional Breakfast Items
                ("Idli Sambar", "₹40", "Steamed rice cakes served with lentil soup and coconut chutney", "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Breakfast,South Indian,Veg"),
                ("Masala Dosa", "₹60", "Crispy rice crepe filled with spiced potato filling", "https://images.unsplash.com/photo-1630409351241-e90e7f5e434d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxEb3NhfGVufDB8fHx8MTc0NDg3MzAwN3ww&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,South Indian,Veg"),
                ("Aloo Paratha", "₹40", "Whole wheat flatbread stuffed with spiced potatoes", "https://images.unsplash.com/photo-1565557623262-b51c2513a641?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Breakfast,North Indian,Veg"),
                ("Upma", "₹30", "Savory semolina porridge with vegetables", "https://i.pinimg.com/736x/98/3e/e4/983ee49c6e2516469a9af13f0a2ccc83.jpg", "Breakfast,South Indian,Veg"),
                ("Vada Pav", "₹25", "Spicy potato fritter in a bun with chutneys", "https://images.unsplash.com/photo-1606491956689-2ea866880c84?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Breakfast,Veg"),
                ("Jain Dosa", "₹50", "Crispy rice crepe without onion and garlic", "https://images.unsplash.com/photo-1630409351241-e90e7f5e434d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxEb3NhfGVufDB8fHx8MTc0NDg3MzAwN3ww&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,South Indian,Jain"),
                ("Sabudana Khichdi", "₹35", "Sago pearls cooked with peanuts and mild spices", "https://images.unsplash.com/photo-1627035537702-ddca174d7987?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxTYWJ1ZGFuYSUyMEtoaWNoZGl8ZW58MHx8fHwxNzQ0ODczMDA4fDA&ixlib=rb-4.0.3&q=80&w=1080", "Breakfast,Jain"),
                
                # Additional Lunch Items
                ("Chole Bhature", "₹70", "Spiced chickpea curry with deep-fried bread", "https://imgs.search.brave.com/QAaF3ShnrO9AUHEBpT6P1iSGfD4fUVymUA2ZgDYwbMk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzEzLzIzLzYzLzgx/LzM2MF9GXzEzMjM2/MzgxMjJfVWkxRG9L/RUxiNWt6aGtCaktI/VEtndnhVdlpGTkRN/cTYuanBn", "Lunch,North Indian,Veg"),
                ("Pav Bhaji", "₹60", "Spiced vegetable mash served with buttered rolls", "https://images.unsplash.com/photo-1606491956391-70868b5d0f47?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxQYXYlMjBCaGFqaXxlbnwwfHx8fDE3NDQ4NzMwMDl8MA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,Veg"),
                ("Thali", "₹120", "Complete meal with rice, dal, vegetables, roti, and dessert", "https://images.unsplash.com/photo-1576846806147-8065a16f89b0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxUaGFsaXxlbnwwfHx8fDE3NDQ4NzMwMTB8MA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,North Indian,Veg"),
                ("Paneer Butter Masala", "₹90", "Cottage cheese cubes in rich tomato gravy", "https://imgs.search.brave.com/Q4VGlWhrqQOgmJAgV44QdURlL8RQiGMonKhYlRN30Uk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzExLzU0LzgzLzg3/LzM2MF9GXzExNTQ4/Mzg3ODBfZE1pdk5E/UXFpUWI1a0dDcGNY/UDR0c0FmSmt5eEJ5/cG8uanBn", "Lunch,North Indian,Veg"),
                ("Dal Makhani", "₹70", "Creamy black lentils simmered overnight", "https://imgs.search.brave.com/Pb3hx7gs3N40h0iGS139W5FiQ891kC_SI1vAWwd70PY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTM2/MDQ1Nzc0My9waG90/by90b3Atdmlldy1v/Zi1kYWFsLW1ha2hh/bmktaW4tYm93bC1h/Z2FpbnN0LWJsdWUt/ZGluaW5nLWNsb3Ro/LmpwZz9zPTYxMng2/MTImdz0wJms9MjAm/Yz1KSW95TGNSUmxP/amQxS19RVHpQUEJf/SU1BOXZ2YWlVakxR/QzV5ZUs2WVdZPQ", "Lunch,North Indian,Veg"),
                ("Butter Chicken", "₹110", "Tandoori chicken in rich tomato gravy", "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxCdXR0ZXIlMjBDaGlja2VufGVufDB8fHx8MTc0NDg3MzAxMXww&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,North Indian,Non Veg"),
                ("Fish Curry", "₹100", "Fresh fish cooked in coconut-based gravy", "https://images.unsplash.com/photo-1620894580123-466ad3a0ca06?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjkxODN8MHwxfHNlYXJjaHwxfHxGaXNoJTIwQ3Vycnl8ZW58MHx8fHwxNzQ0ODczMDEyfDA&ixlib=rb-4.0.3&q=80&w=1080", "Lunch,South Indian,Non Veg"),
                ("Jain Rajma Chawal", "₹80", "Kidney beans curry without onion/garlic served with rice", "https://imgs.search.brave.com/1pk6k_4DZK3b4jswkCELw-fRmeaSFTqU_2-kNvP_yN0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9saDMu/Z29vZ2xldXNlcmNv/bnRlbnQuY29tL3Rn/bnl1ZlQyam9lb2ZF/MEtMa2Z1Ukx3QXhV/MkNNRm82cC1WMDR3/Q0hXQ3IzTmx0cTBU/LXlWYVlrdkRnei1w/Z3ZvQmVkTC15bXN0/anBEdkFkcnRPek9t/SnlVeFVtYm1USkRZ/ZTFOb0NqeGc9dzUx/Mi1ydw", "Lunch,North Indian,Jain"),
                
                # Additional Chinese Items
                ("Veg Hakka Noodles", "₹50", "Stir-fried noodles with vegetables", "https://images.unsplash.com/photo-1585032226651-759b368d7246?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Chinese,Veg"),
                ("Veg Manchurian", "₹80", "Vegetable balls in spicy, sweet and sour sauce", "https://imgs.search.brave.com/sMQc73tPO3LwzU5FMY7TIMo6ag2zw7l99lM9WcLcusw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTMz/NDExNDQ0MS9waG90/by9jYWJiYWdlLW1h/bmNodXJpYW4uanBn/P3M9NjEyeDYxMiZ3/PTAmaz0yMCZjPUNG/NzhyS2VIb01hUTBN/MlRONGJlQzNZc1o4/UF84bzAtTERpOUlk/ckxVX0k9", "Chinese,Veg"),
                ("Gobi Manchurian", "₹70", "Cauliflower florets in spicy Indo-Chinese sauce", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Chinese,Veg"),
                ("Veg Spring Rolls", "₹50", "Crispy rolls filled with vegetables", "https://images.unsplash.com/photo-1626074353765-517a681e40be?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Chinese,Veg"),
                ("Schezwan Fried Rice", "₹70", "Spicy fried rice with Schezwan sauce", "https://images.unsplash.com/photo-1603133872878-684f208fb84b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Chinese,Veg"),
                ("Chilli Chicken", "₹90", "Spicy chicken with bell peppers", "https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Chinese,Non Veg"),
                ("Chicken Hakka Noodles", "₹80", "Stir-fried noodles with chicken", "https://images.unsplash.com/photo-1585032226651-759b368d7246?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Chinese,Non Veg"),
                ("Jain Manchurian", "₹70", "Indo-Chinese dish prepared without onion and garlic", "https://imgs.search.brave.com/sMQc73tPO3LwzU5FMY7TIMo6ag2zw7l99lM9WcLcusw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTMz/NDExNDQ0MS9waG90/by9jYWJiYWdlLW1h/bmNodXJpYW4uanBn/P3M9NjEyeDYxMiZ3/PTAmaz0yMCZjPUNG/NzhyS2VIb01hUTBN/MlRONGJlQzNZc1o4/UF84bzAtTERpOUlk/ckxVX0k9", "Chinese,Jain"),
                
                # Additional Drinks Items
                ("Masala Chai", "₹15", "Indian spiced tea", "https://images.unsplash.com/photo-1561336526-2914f13ceb36?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Veg"),
                ("Lassi", "₹30", "Sweet yogurt-based drink", "https://images.unsplash.com/photo-1541658016709-82535e94bc69?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Veg"),
                ("Fresh Lime Soda", "₹25", "Refreshing lime and soda drink", "https://images.unsplash.com/photo-1543253687-c931c8e01820?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Veg"),
                ("Buttermilk", "₹20", "Spiced yogurt drink", "https://images.unsplash.com/photo-1553530758-b61f8c2a5a3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Veg"),
                ("Mango Shake", "₹40", "Fresh mango blended with milk", "https://images.unsplash.com/photo-1546173159-315724a31696?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Veg"),
                ("Rose Milk", "₹35", "Chilled milk flavored with rose syrup", "https://images.unsplash.com/photo-1563805042-7684c019e1cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Veg"),
                ("Jain Lassi", "₹30", "Yogurt-based drink prepared with Jain principles", "https://images.unsplash.com/photo-1541658016709-82535e94bc69?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Drinks,Jain"),
                
                # Additional Dessert Items
                ("Gulab Jamun", "₹30", "Deep-fried milk solids soaked in sugar syrup", "https://images.unsplash.com/photo-1601303516533-6e592999c452?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Veg"),
                ("Rasgulla", "₹30", "Soft cheese balls in sugar syrup", "https://images.unsplash.com/photo-1627014610728-7cb929ad48aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Veg"),
                ("Jalebi", "₹25", "Crispy, syrup-soaked spiral sweets", "https://images.unsplash.com/photo-1589249125609-c683e9209d23?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Veg"),
                ("Kheer", "₹35", "Rice pudding with nuts", "https://images.unsplash.com/photo-1634116518069-ca380afba2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Veg"),
                ("Kulfi", "₹40", "Traditional Indian ice cream", "https://images.unsplash.com/photo-1627014611763-62bbef12d619?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Veg"),
                ("Gajar Ka Halwa", "₹40", "Sweet carrot pudding", "https://images.unsplash.com/photo-1610063633845-e3f1e94b98e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Veg"),
                ("Jain Kheer", "₹35", "Rice pudding prepared without vanilla essence", "https://images.unsplash.com/photo-1634116518069-ca380afba2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "Dessert,Jain"),
                
                # Additional South Indian Items (New category)
                ("Medu Vada", "₹30", "Savory lentil donuts", "https://images.unsplash.com/photo-1630383249896-981686ae8a76?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Veg"),
                ("Uttapam", "₹55", "Thick pancake topped with vegetables", "https://images.unsplash.com/photo-1630409351217-bc4fa6422075?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Veg"),
                ("Sambhar Rice", "₹60", "Rice served with lentil stew", "https://images.unsplash.com/photo-1605196560547-1f58f7e07645?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Lunch,Veg"),
                ("Rasam", "₹30", "Spicy tamarind soup", "https://images.unsplash.com/photo-1606025682478-cc91dabf6968?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Veg"),
                ("Appam", "₹40", "Fermented rice pancake with coconut milk", "https://images.unsplash.com/photo-1626777536136-36a8400c8bb1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Veg"),
                ("Chicken Chettinad", "₹100", "Spicy chicken curry from Tamil Nadu", "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Non Veg"),
                ("Jain Uttapam", "₹50", "Thick pancake without onion and garlic", "https://images.unsplash.com/photo-1630409351217-bc4fa6422075?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "South Indian,Jain"),
                
                # Additional North Indian Items (New category)
                ("Butter Naan", "₹20", "Leavened flatbread cooked in tandoor", "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Veg"),
                ("Kadai Paneer", "₹90", "Cottage cheese cooked with bell peppers", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Veg"),
                ("Shahi Paneer", "₹90", "Cottage cheese in creamy gravy", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Veg"),
                ("Rajma Chawal", "₹80", "Kidney beans curry served with rice", "https://images.unsplash.com/photo-1612204104655-6c8a57ae235e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Lunch,Veg"),
                ("Aloo Gobi", "₹70", "Potato and cauliflower curry", "https://images.unsplash.com/photo-1601050690597-df0568f70950?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Veg"),
                ("Chicken Biryani", "₹120", "Fragrant rice dish with chicken", "https://images.unsplash.com/photo-1589302168068-964664d93dc0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Non Veg"),
                ("Mutton Rogan Josh", "₹130", "Kashmiri lamb curry", "https://images.unsplash.com/photo-1626777536136-36a8400c8bb1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Non Veg"),
                ("Jain Aloo Gobi", "₹70", "Potato and cauliflower curry without onion/garlic", "https://images.unsplash.com/photo-1601050690597-df0568f70950?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80", "North Indian,Jain")
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
        return  ["All", "Breakfast", "Lunch", "Veg", "Non Veg", "Jain", "North Indian", "South Indian", "Chinese", "Drinks", "Dessert"]

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

    def get_all_items(self):
        """Return all menu items."""
        return self.menu_items