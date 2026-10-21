-- ============================================
-- PROJECT 6: Large Sales Data Warehouse
-- ============================================

-- ============================================
-- DIMENSION TABLES
-- ============================================

-- Customer Dimension
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name TEXT
);

-- Product Dimension
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name TEXT,
    category TEXT
);

-- Date Dimension
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    order_date DATE
);

-- ============================================
-- FACT TABLE
-- ============================================

-- Sales Fact Table
CREATE TABLE fact_sales (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    date_id INT REFERENCES dim_date(date_id),
    quantity INT,
    price FLOAT,
    revenue FLOAT
);