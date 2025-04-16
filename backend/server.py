from flask import Flask, request, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../database/canteen.db')

@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()
    print('Received order:', order_data)
    # Extract order fields
    items = json.dumps(order_data.get('items', []))
    special_instructions = order_data.get('special_instructions', '')
    total = order_data.get('total', 0.0)
    # Insert into database
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO orders (items, special_instructions, total)
            VALUES (?, ?, ?)
        ''', (items, special_instructions, total))
        order_id = c.lastrowid  # Get the last inserted order ID
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Order received', 'order_id': order_id}), 201
    except Exception as e:
        print('DB Error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to save order'}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, items, special_instructions, total, payment_status FROM orders')
        rows = c.fetchall()
        conn.close()
        orders = []
        for row in rows:
            orders.append({
                'id': row[0],
                'items': json.loads(row[1]),
                'special_instructions': row[2],
                'total': row[3],
                'payment_status': row[4]
            })
        return jsonify({'status': 'success', 'orders': orders}), 200
    except Exception as e:
        print('DB Error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to fetch orders'}), 500

@app.route('/orders/<int:order_id>/pay', methods=['POST'])
def mark_order_paid(order_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE orders SET payment_status = ? WHERE id = ?', ('paid', order_id))
        conn.commit()
        updated = c.rowcount
        conn.close()
        if updated:
            return jsonify({'status': 'success', 'message': f'Order {order_id} marked as paid'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    except Exception as e:
        print('DB Error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to update payment status'}), 500

@app.route('/orders/<int:order_id>/status', methods=['GET'])
def get_payment_status(order_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT payment_status FROM orders WHERE id = ?', (order_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return jsonify({'status': 'success', 'payment_status': row[0]}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    except Exception as e:
        print('DB Error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to fetch payment status'}), 500

@app.route('/menu-items', methods=['POST'])
def add_menu_item():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description', '')
    image_url = data.get('image_url', '')
    category = data.get('category', '')
    if not name or not price or not category:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO menu_items (name, price, description, image_url, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, description, image_url, category))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Menu item added'}), 201
    except Exception as e:
        print('DB Error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to add menu item'}), 500

@app.route('/menu-items', methods=['GET'])
def get_menu_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, name, price, description, image_url, category FROM menu_items')
        rows = c.fetchall()
        conn.close()
        items = []
        for row in rows:
            items.append({
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'description': row[3],
                'image_url': row[4],
                'category': row[5]
            })
        return jsonify({'status': 'success', 'items': items}), 200
    except Exception as e:
        print('DB Error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to fetch menu items'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
