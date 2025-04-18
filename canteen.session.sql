
DELETE FROM menu_items;
DELETE FROM sqlite_sequence WHERE name='menu_items';

SELECT * FROM menu_items;
SELECT * FROM users;

SELECT * FROM orders;

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    items TEXT NOT NULL, -- JSON string of items
    special_instructions TEXT,
    total REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE orders DROP COLUMN status; 
ALTER TABLE orders ADD COLUMN payment_status TEXT DEFAULT 'unpaid'; 
UPDATE orders SET payment_status = 'unpaid' WHERE id = 1;

-- Truncate orders table (delete all rows but keep the structure)
DELETE FROM orders;
DELETE FROM sqlite_sequence WHERE name='orders';


DELETE from menu_items where id = 67;
-- Reset the sequence counter for menu_items to 63
-- This will make the next inserted item have ID 64
INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('menu_items', 63);
