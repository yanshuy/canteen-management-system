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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
