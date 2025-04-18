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
                ("Pancakes", "₹50", "Fluffy pancakes with maple syrup", 'https://cdn.loveandlemons.com/wp-content/uploads/2025/01/pancake-recipe.jpg', "Breakfast,Veg"),
                ("Sandwich", "₹35", "Club sandwich with fries", 'https://www.watermelon.org/wp-content/uploads/2023/02/Sandwich_2023.jpg', "Lunch,Non Veg"),
                ("Coffee", "₹10", "Freshly brewed coffee", 'https://images.squarespace-cdn.com/content/v1/636bcbc6e2494c61701cfca1/e14a2cb4-1c7b-4ff6-b81a-8cc890f22c46/4212NEW.jpg', "Drinks,Veg"),
                ("Fried Rice", "₹60", "Vegetable fried rice", 'https://cdn.apartmenttherapy.info/image/upload/f_auto,q_auto:eco,c_fill,g_auto,w_1500,ar_3:2/k%2FPhoto%2FRecipes%2F2024-04-fried-rice%2Ffried-rice-060', "Chinese,Veg"),
                ("Cake", "₹40", "Chocolate cake slice", 'https://www.simplyrecipes.com/thmb/sgR08l6hzfOYVqOF-igabSkBm9Q=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Guinness-Cake-LEAD-03-57f370eaacbe474cbfc5d9de224ebd89.jpg', "Dessert,Veg"),
                ("Salad", "₹20", "Greek salad", 'https://cdn.loveandlemons.com/wp-content/uploads/2019/07/salad.jpg', "Other,Veg"),
                ("Omelette", "₹20", "Three-egg omelette with toast", 'https://images.squarespace-cdn.com/content/v1/6109e64cfe878a0cad199515/e9272543-023a-49c0-9bec-89af5bd8aea3/Souffle+Omellette-1.jpg', "Breakfast,Non Veg"),
                ("Pasta", "₹50", "Spaghetti carbonara", 'https://cache.dominos.com/olo/6_153_2/assets/build/market/US/_en/images/img/products/larges/S_5CHSMAC.jpg', "Lunch,Non Veg"),
                ("Smoothie", "₹20", "Mixed berry smoothie", 'https://media.bluediamond.com/uploads/2023/01/24174916/Strawberry_Banana_Smoothie_sm.jpg', "Drinks,Veg"),
                ("Chilli Paneer", "₹70", "Spicy paneer with bell peppers", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2022/02/chilli-paneer-recipe.jpg', "Chinese,Lunch,Jain"),
                ("Jain Poha", "₹30", "Poha prepared Jain style without onions and potatoes", 'https://img-global.cpcdn.com/recipes/28ba34e738307ca3/680x482cq70/jain-poha-recipe-main-photo.jpg', "Breakfast,Jain"),
                ("Idli Sambar", "₹40", "Steamed rice cakes served with lentil soup and coconut chutney", 'https://mayuris-jikoni.com/wp-content/uploads/2012/06/idli-sambar-1-copy.jpg', "Breakfast,South Indian,Veg"),
                ("Masala Dosa", "₹60", "Crispy rice crepe filled with spiced potato filling", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2021/06/masala-dosa-recipe.jpg', "Breakfast,South Indian,Veg"),
                ("Aloo Paratha", "₹40", "Whole wheat flatbread stuffed with spiced potatoes", 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Aloo_Paratha_also_known_as_Batatay_Jo_Phulko.jpg/960px-Aloo_Paratha_also_known_as_Batatay_Jo_Phulko.jpg', "Breakfast,North Indian,Veg"),
                ("Upma", "₹30", "Savory semolina porridge with vegetables", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2021/12/quinoa-upma-recipe.jpg', "Breakfast,South Indian,Veg"),
                ("Vada Pav", "₹25", "Spicy potato fritter in a bun with chutneys", 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Vada_Pav-Indian_street_food.JPG/1200px-Vada_Pav-Indian_street_food.JPG', "Breakfast,Veg"),
                ("Jain Dosa", "₹50", "Crispy rice crepe without onion and garlic", 'https://i.ytimg.com/vi/28D5OofiGLI/maxresdefault.jpg', "Breakfast,South Indian,Jain"),
                ("Sabudana Khichdi", "₹35", "Sago pearls cooked with peanuts and mild spices", 'https://www.ohmyveg.co.uk/wp-content/uploads/2021/01/sabudana-khichdi-e1722865389647-735x735.jpg', "Breakfast,Jain"),
                ("Chole Bhature", "₹70", "Spiced chickpea curry with deep-fried bread", 'https://i.ytimg.com/vi/wAv-mFU7eus/maxresdefault.jpg', "Lunch,North Indian,Veg"),
                ("Pav Bhaji", "₹60", "Spiced vegetable mash served with buttered rolls", 'https://www.cookwithmanali.com/wp-content/uploads/2018/05/Best-Pav-Bhaji-Recipe.jpg', "Lunch,Veg"),
                ("Thali", "₹120", "Complete meal with rice, dal, vegetables, roti, and dessert", 'https://www.rajwadithali.com/Restaurants/RJT-RajwadiThali/Images/IndexPageImages/02.jpg', "Lunch,North Indian,Veg"),
                ("Paneer Butter Masala", "₹90", "Cottage cheese cubes in rich tomato gravy", 'https://www.cookwithmanali.com/wp-content/uploads/2019/05/Paneer-Butter-Masala.jpg', "Lunch,North Indian,Veg"),
                ("Dal Makhani", "₹70", "Creamy black lentils simmered overnight", 'https://www.cookwithmanali.com/wp-content/uploads/2019/04/Restaurant-Style-Dal-Makhani.jpg', "Lunch,North Indian,Veg"),
                ("Butter Chicken", "₹110", "Tandoori chicken in rich tomato gravy", 'https://cdn.apartmenttherapy.info/image/upload/f_jpg,q_auto:eco,c_fill,g_auto,w_1500,ar_1:1/k%2FPhoto%2FRecipes%2F2024-12-butter-chicken%2Fbutter-chicken-323', "Lunch,North Indian,Non Veg"),
                ("Fish Curry", "₹100", "Fresh fish cooked in coconut-based gravy", 'https://stewwithsaba.com/wp-content/uploads/2024/05/IMG_4409-edited.jpg', "Lunch,South Indian,Non Veg"),
                ("Jain Rajma Chawal", "₹80", "Kidney beans curry without onion/garlic served with rice", 'https://www.sailusfood.com/wp-content/uploads/2015/07/rajma-recipe.jpg', "Lunch,North Indian,Jain"),
                ("Veg Hakka Noodles", "₹50", "Stir-fried noodles with vegetables", 'https://thechutneylife.com/wp-content/uploads/2017/09/TYFNgSGl-scaled.jpeg', "Chinese,Veg"),
                ("Veg Manchurian", "₹80", "Vegetable balls in spicy, sweet and sour sauce", 'https://i.ytimg.com/vi/xkMbJCtaaqA/hq720.jpg?sqp=-…ADIQj0AgKJD&rs=AOn4CLDrMLgdijp9TJ92IUYugdtisp2tIw', "Chinese,Veg"),
                ("Veg Spring Rolls", "₹50", "Crispy rolls filled with vegetables", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2022/04/spring-rolls-with-vegetables.jpg', "Chinese,Veg"),
                ("Schezwan Fried Rice", "₹70", "Spicy fried rice with Schezwan sauce", 'https://imgs.search.brave.com/9pspMXnzEjOflZ3TL6Bv5-m_H4Vk5KMQYTYLNiT8N9s/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/d2hpc2thZmZhaXIu/Y29tL3dwLWNvbnRl/bnQvdXBsb2Fkcy8y/MDIwLzA5L1NjaGV6/d2FuLUZyaWVkLVJp/Y2UtMi0xLmpwZw', "Chinese,Veg"),
                ("Chilli Chicken", "₹90", "Spicy chicken with bell peppers", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2023/12/chilli-chicken-recipe.webp', "Chinese,Non Veg"),
                ("Chicken Hakka Noodles", "₹80", "Stir-fried noodles with chicken", 'https://static.toiimg.com/photo/75356205.cms', "Chinese,Non Veg"),
                ("Jain Manchurian", "₹70", "Indo-Chinese dish prepared without onion and garlic", 'https://i.pinimg.com/564x/96/52/90/965290464c2be01d38a80126cbbb8f3c.jpg', "Chinese,Jain"),
                ("Masala Chai", "₹15", "Indian spiced tea", 'https://shivanilovesfood.com/wp-content/uploads/2022/08/Chai-6.jpg', "Drinks,Veg"),
                ("Lassi", "₹30", "Sweet yogurt-based drink", 'https://ethnicspoon.com/wp-content/uploads/2014/08/lassi.jpg', "Drinks,Veg"),
                ("Fresh Lime Soda", "₹25", "Refreshing lime and soda drink", 'https://i.ytimg.com/vi/s5uPpSAVORw/sddefault.jpg', "Drinks,Veg"),
                ("Buttermilk", "₹20", "Spiced yogurt drink", 'https://res.cloudinary.com/kraft-heinz-whats-cooking-ca/image/upload/f_auto/q_auto/r_8/c_limit,w_3840/f_auto/q_auto/v1/dxp-images/brands/products/00021000643462-buttermilk-ranch-dressing/marketing-view-color-front_content-hub-9700492_b2de2add653ff8184f8e6ad9f1c31766?_a=BAVAfVDW0', "Drinks,Veg"),
                ("Mango Shake", "₹40", "Fresh mango blended with milk", 'https://bombayrestaurantac.com/wp-content/uploads/2023/06/mango-shake-image.jpeg', "Drinks,Veg"),
                ("Rose Milk", "₹35", "Chilled milk flavored with rose syrup", 'https://www.yummytummyaarthi.com/wp-content/uploads/2023/09/rose-milk-1.jpg', "Drinks,Veg"),
                ("Jain Lassi", "₹30", "Yogurt-based drink prepared with Jain principles", 'https://www.jaindairy.com/wp-content/uploads/2021/03/RAJWADI-LASSI.jpeg', "Drinks,Jain"),
                ("Gulab Jamun", "₹30", "Deep-fried milk solids soaked in sugar syrup", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2021/11/gulab-jamun.webp', "Dessert,Veg"),
                ("Rasgulla", "₹30", "Soft cheese balls in sugar syrup", 'https://cdn.uengage.io/uploads/28289/image-AGXRCD-1696400439.jpg', "Dessert,Veg"),
                ("Jalebi", "₹25", "Crispy, syrup-soaked spiral sweets", 'https://www.chhappanbhog.com/wp-content/uploads/2022/05/Coine-Jalebi.jpg', "Dessert,Veg"),
                ("Kheer", "₹35", "Rice pudding with nuts", 'https://shivanilovesfood.com/wp-content/uploads/2024/01/Creamy-Kheer-4.jpg', "Dessert,Veg"),
                ("Kulfi", "₹40", "Traditional Indian ice cream", 'https://limethyme.com/wp-content/uploads/2021/06/Mango-kulfi-1.jpg', "Dessert,Veg"),
                ("Gajar Ka Halwa", "₹40", "Sweet carrot pudding", 'https://i0.wp.com/kalimirchbysmita.com/wp-content/uploads/2016/01/Gajar-ka-Halwa-03-1024x683.jpg?resize=1024%2C683', "Dessert,Veg"),
                ("Jain Kheer", "₹35", "Rice pudding prepared without vanilla essence", 'https://img-global.cpcdn.com/recipes/23f1faee02c645cb/680x482cq70/kheer-recipe-main-photo.jpg', "Dessert,Jain"),
                ("Medu Vada", "₹30", "Savory lentil donuts", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2014/07/medu-vada-recipe-500x500.jpg', "South Indian,Veg"),
                ("Uttapam", "₹55", "Thick pancake topped with vegetables", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2022/07/uttapam-recipe-with-podi.webp', "South Indian,Veg"),
                ("Sambhar Rice", "₹60", "Rice served with lentil stew", 'https://rakskitchen.net/wp-content/uploads/2011/03/sambar-sadam_thumb4.jpg', "South Indian,Lunch,Veg"),
                ("Rasam", "₹30", "Spicy tamarind soup", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2022/01/rasam.webp', "South Indian,Veg"),
                ("Appam", "₹40", "Fermented rice pancake with coconut milk", 'https://www.mydiversekitchen.com/wp-content/uploads/2008/08/Appam-and-Ishtu-1.jpeg', "South Indian,Veg"),
                ("Jain Uttapam", "₹50", "Thick pancake without onion and garlic", 'https://img-global.cpcdn.com/recipes/1fe6b1dd2ba6e1ce/680x482cq70/tomato-cabbage-capsicum-jain-uttapam-recipe-main-photo.jpg', "South Indian,Jain"),
                ("Butter Naan", "₹20", "Leavened flatbread cooked in tandoor", 'https://www.indianhealthyrecipes.com/wp-content/uploads/2022/03/butter-naan.jpg', "North Indian,Veg"),
                ("Kadai Paneer", "₹90", "Cottage cheese cooked with bell peppers", 'https://www.cookwithmanali.com/wp-content/uploads/2017/03/Best-Kadai-Paneer.jpg', "North Indian,Veg"),
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