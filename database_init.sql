-- Create Database
CREATE DATABASE IF NOT EXISTS oil_shop_db;
USE oil_shop_db;

-- Drop tables if they exist (for fresh installation)
DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS employees;

-- Create Suppliers Table
CREATE TABLE suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Products Table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    barcode VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    cost_price DECIMAL(10, 2) DEFAULT 0,
    quantity INT DEFAULT 0,
    min_stock_level INT DEFAULT 10,
    supplier_id INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL,
    INDEX idx_barcode (barcode),
    INDEX idx_category (category),
    INDEX idx_quantity (quantity)
);

-- Create Employees Table
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Sales Table
CREATE TABLE sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(255) DEFAULT 'Walk-in',
    customer_phone VARCHAR(20),
    total_amount DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    payment_method ENUM('cash', 'card', 'online') DEFAULT 'cash',
    employee_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE SET NULL,
    INDEX idx_date (created_at),
    INDEX idx_employee (employee_id)
);

-- Create Sale Items Table
CREATE TABLE sale_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_sale (sale_id),
    INDEX idx_product (product_id)
);

-- Insert Default Admin User will be created by fix_admin_password.py script
-- This ensures the password hash is compatible with your Werkzeug version

-- Insert Sample Suppliers
INSERT INTO suppliers (name, contact_person, phone, email, address) VALUES
('Shell Oil Distributors', 'John Smith', '555-0101', 'john@shell.com', '123 Main St, City'),
('Mobil Oil Supply', 'Jane Doe', '555-0102', 'jane@mobil.com', '456 Oak Ave, City'),
('Castrol Industries', 'Bob Johnson', '555-0103', 'bob@castrol.com', '789 Pine Rd, City');

-- Insert Sample Products
INSERT INTO products (name, barcode, category, price, cost_price, quantity, min_stock_level, supplier_id, description) VALUES
('Shell Helix Ultra 5W-40', '1234567890123', 'Engine Oil', 45.99, 32.00, 50, 10, 1, 'Premium synthetic engine oil'),
('Mobil 1 ESP 5W-30', '1234567890124', 'Engine Oil', 42.50, 29.50, 45, 10, 2, 'Advanced full synthetic engine oil'),
('Castrol GTX 10W-40', '1234567890125', 'Engine Oil', 35.99, 24.00, 60, 15, 3, 'Premium conventional motor oil'),
('Shell Rimula R6 LM', '1234567890126', 'Diesel Oil', 89.99, 65.00, 30, 8, 1, 'Heavy-duty diesel engine oil'),
('Mobil Delvac MX 15W-40', '1234567890127', 'Diesel Oil', 82.50, 58.00, 35, 8, 2, 'Diesel engine protection'),
('Castrol Power 1 Racing 4T', '1234567890128', 'Motorcycle Oil', 38.99, 26.00, 40, 10, 3, '4-stroke motorcycle oil'),
('Shell Advance Ultra 4', '1234567890129', 'Motorcycle Oil', 41.50, 28.50, 38, 10, 1, 'Premium motorcycle engine oil'),
('Mobil Super 3000 X1', '1234567890130', 'Engine Oil', 39.99, 27.00, 55, 12, 2, 'Synthetic engine oil'),
('Castrol Magnatec 5W-30', '1234567890131', 'Engine Oil', 44.99, 31.00, 42, 10, 3, 'Intelligent molecules protection'),
('Shell Helix HX7 10W-40', '1234567890132', 'Engine Oil', 34.99, 23.50, 65, 15, 1, 'Semi-synthetic motor oil'),
('Hydraulic Oil ISO 68', '1234567890133', 'Hydraulic Oil', 55.99, 38.00, 25, 8, 2, 'Industrial hydraulic oil'),
('Gear Oil 80W-90', '1234567890134', 'Gear Oil', 28.99, 19.00, 48, 12, 3, 'Automotive gear oil'),
('2-Stroke Oil', '1234567890135', 'Engine Oil', 22.99, 15.00, 70, 20, 1, 'High-performance 2-stroke oil'),
('ATF Dexron III', '1234567890136', 'Transmission Oil', 32.99, 22.00, 52, 12, 2, 'Automatic transmission fluid'),
('Brake Fluid DOT 4', '1234567890137', 'Brake Fluid', 18.99, 12.00, 80, 20, 3, 'High-performance brake fluid');

-- Insert Sample Sales (for demonstration)
INSERT INTO sales (customer_name, customer_phone, total_amount, discount, payment_method, employee_id) VALUES
('John Customer', '555-1234', 91.98, 0, 'cash', 1),
('Jane Smith', '555-5678', 135.97, 5.00, 'card', 1);

INSERT INTO sale_items (sale_id, product_id, quantity, price, subtotal) VALUES
(1, 1, 2, 45.99, 91.98),
(2, 4, 1, 89.99, 89.99),
(2, 1, 1, 45.99, 45.99);

-- Create Views for Reporting

-- Sales Summary View
CREATE OR REPLACE VIEW sales_summary AS
SELECT 
    DATE(s.created_at) as sale_date,
    COUNT(s.id) as total_transactions,
    SUM(s.total_amount) as total_sales,
    SUM(s.discount) as total_discounts,
    AVG(s.total_amount) as average_sale
FROM sales s
GROUP BY DATE(s.created_at)
ORDER BY sale_date DESC;

-- Product Sales Summary View
CREATE OR REPLACE VIEW product_sales_summary AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.barcode,
    SUM(si.quantity) as total_sold,
    SUM(si.subtotal) as total_revenue,
    p.quantity as current_stock
FROM products p
LEFT JOIN sale_items si ON p.id = si.product_id
GROUP BY p.id, p.name, p.category, p.barcode, p.quantity
ORDER BY total_sold DESC;

-- Low Stock Alert View
CREATE OR REPLACE VIEW low_stock_alerts AS
SELECT 
    id,
    name,
    barcode,
    category,
    quantity,
    min_stock_level,
    (min_stock_level - quantity) as stock_deficit
FROM products
WHERE quantity <= min_stock_level
ORDER BY stock_deficit DESC;

-- Monthly Sales Report View
CREATE OR REPLACE VIEW monthly_sales_report AS
SELECT 
    YEAR(s.created_at) as year,
    MONTH(s.created_at) as month,
    COUNT(s.id) as total_transactions,
    SUM(s.total_amount) as total_sales,
    SUM(si.quantity) as total_items_sold,
    COUNT(DISTINCT s.employee_id) as active_employees
FROM sales s
LEFT JOIN sale_items si ON s.id = si.sale_id
GROUP BY YEAR(s.created_at), MONTH(s.created_at)
ORDER BY year DESC, month DESC;