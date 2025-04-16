from datetime import datetime
import os

class InvoiceGenerator:
    def __init__(self, cart_items, menu_service, special_instructions="", order_id=None):
        self.cart_items = cart_items
        self.menu_service = menu_service
        self.special_instructions = special_instructions
        self.order_id = order_id
        
        # Ensure the invoices directory exists in static folder
        self.invoices_dir = os.path.join("static", "invoices")
        os.makedirs(self.invoices_dir, exist_ok=True)
    
    def generate_invoice(self):
        """Generate an HTML invoice and save it to a file"""
        # Generate a unique filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        invoice_filename = f"invoice_{timestamp}.html"
        invoice_path = os.path.join(self.invoices_dir, invoice_filename)
        
        # Calculate invoice details
        invoice_data = self._calculate_invoice_data()
        
        # Generate the HTML content
        html_content = self._generate_html_invoice(invoice_data, timestamp, self.order_id)
        
        # Write to file
        with open(invoice_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return invoice_path
    
    def _calculate_invoice_data(self):
        """Calculate subtotal, tax, and total for the invoice"""
        items_details = []
        subtotal = 0
        
        for item_name, quantity in self.cart_items.items():
            # Find the menu item details
            menu_item = next((item for item in self.menu_service.get_all_items() 
                             if item["name"] == item_name), None)
            
            if menu_item:
                price_text = menu_item["price"]
                price_value = float(price_text.replace("₹", ""))
                item_total = price_value * quantity
                subtotal += item_total
                
                items_details.append({
                    "name": item_name,
                    "price": price_value,
                    "quantity": quantity,
                    "total": item_total
                })
        
        tax_rate = 0.05
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        return {
            "items": items_details,
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax": tax,
            "total": total,
            "special_instructions": self.special_instructions
        }
    
    def _generate_html_invoice(self, data, timestamp, order_id=None):
        """Generate the HTML content for the invoice"""
        invoice_date = datetime.now().strftime("%B %d, %Y %I:%M %p")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order No: {order_id if order_id is not None else timestamp}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .invoice-container {{
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            padding: 40px;
            margin-bottom: 30px;
        }}
        .invoice-header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #FF8C32;
            padding-bottom: 20px;
            color: #FF8C32;
        }}
        .invoice-header h1 {{
            margin-bottom: 5px;
            color: #FF8C32;
        }}
        .invoice-header h2 {{
            margin-top: 0;
            font-weight: 400;
            color: #666;
        }}
        .invoice-details {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 15px;
            text-align: left;
        }}
        th {{
            background-color: #FF8C32;
            color: white;
            font-weight: 500;
        }}
        tr:nth-child(even) {{
            background-color: #f7f7f7;
        }}
        .text-right {{
            text-align: right;
        }}
        .total-row {{
            font-weight: bold;
            font-size: 1.1em;
            background-color: #f2f2f2;
        }}
        .total-row td {{
            border-top: 2px solid #ddd;
        }}
        .instructions {{
            background-color: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #FF8C32;
        }}
        .footer {{
            margin-top: 50px;
            text-align: center;
            font-size: 0.9em;
            color: #777;
            border-top: 1px solid #ddd;
            padding-top: 30px;
        }}
        @media print {{
            body {{
                background-color: white;
                padding: 0;
            }}
            .invoice-container {{
                box-shadow: none;
                padding: 0;
            }}
            .no-print {{
                display: none;
            }}
        }}
        .print-button {{
            background-color: #38B000;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin-top: 20px;
            transition: background-color 0.3s;
        }}
        .print-button:hover {{
            background-color: #2D9300;
        }}
        .logo {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="invoice-container">
        <div class="invoice-header">
            <div class="logo">🍽️</div>
            <h1>Canteeny</h1>
            <h2>INVOICE</h2>
            <p>Order No: {order_id if order_id is not None else timestamp}</p>
            <p>Date: {invoice_date}</p>
        </div>
        
        <div class="invoice-details">
            <div>
                <h3>From:</h3>
                <p>Canteeny Food Services<br>
                123 College Road<br>
                Campus Plaza, Building 4<br>
                Phone: 7930874211</p>
            </div>
            <div>
                <h3>To:</h3>
                <p>Valued Customer<br>
                Thank you for your order!</p>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 40%;">Item</th>
                    <th style="width: 20%;">Price</th>
                    <th style="width: 15%;">Quantity</th>
                    <th style="width: 25%;">Total</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add items rows
        for item in data["items"]:
            html += f"""
                <tr>
                    <td>{item['name']}</td>
                    <td>₹{item['price']:.2f}</td>
                    <td>{item['quantity']}</td>
                    <td>₹{item['total']:.2f}</td>
                </tr>"""
        
        # Add summary rows
        html += f"""
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="3" class="text-right">Subtotal:</td>
                    <td>₹{data['subtotal']:.2f}</td>
                </tr>
                <tr>
                    <td colspan="3" class="text-right">Tax ({data['tax_rate']*100:.0f}%):</td>
                    <td>₹{data['tax']:.2f}</td>
                </tr>
                <tr class="total-row">
                    <td colspan="3" class="text-right">Total:</td>
                    <td>₹{data['total']:.2f}</td>
                </tr>
            </tfoot>
        </table>
"""
        
        # Add special instructions if provided
        if data["special_instructions"]:
            html += f"""
        <div class="instructions">
            <h3>Special Instructions:</h3>
            <p>{data['special_instructions']}</p>
        </div>
"""
        
        # Add footer and print button
        html += """
        <div class="no-print" style="text-align: center; margin: 30px 0;">
            <button class="print-button" onclick="window.print();">Print Invoice</button>
        </div>
        
        <div class="footer">
            <p>For any issues with your order, please contact us at 7930874211.</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
