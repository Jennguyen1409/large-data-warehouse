
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os


os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/load_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_data(file_path):
    """Read the raw CSV file"""
    # Define the exact column names
    columns = ['sale_id', 'date', 'customer_id', 'product_id', 'category', 
               'quantity', 'unit_price', 'payment_method', 'status', 'store', 'revenue']
    
    # Read the CSV, forcing the columns (since the header is missing in Docker)
    df = pd.read_csv(file_path, names=columns, header=None)
    
    logging.info(f"Data extracted. Rows: {len(df)}")
    print(f"✅ Extracted {len(df)} rows")
    print(f"✅ Columns: {list(df.columns)}")
    return df

def transform_data(df):
    """Transform raw data into star schema tables"""
    
    # 1. Customer Dimension
    customers = df[['customer_id']].drop_duplicates().reset_index(drop=True)
    customers['customer_name'] = 'Customer_' + customers['customer_id'].astype(str)
    customers = customers[['customer_id', 'customer_name']]
    print(f"✅ Created dim_customer: {len(customers)} rows")
    
    # 2. Product Dimension
    products = df[['product_id', 'category']].drop_duplicates().reset_index(drop=True)
    products['product_name'] = 'Product_' + products['product_id'].astype(str)
    products = products[['product_id', 'product_name', 'category']]
    print(f"✅ Created dim_product: {len(products)} rows")
    
    # 3. Date Dimension
    dates = df[['date']].drop_duplicates().reset_index(drop=True)
    dates['date_id'] = dates.index + 1
    dates = dates.rename(columns={'date': 'order_date'})
    dates = dates[['date_id', 'order_date']]
    print(f"✅ Created dim_date: {len(dates)} rows")
    
    # 4. Fact Table
    fact = df.copy()
    
    fact = fact.merge(dates, left_on='date', right_on='order_date', how='left')
    
    fact = fact[['sale_id', 'customer_id', 'product_id', 'date_id', 'quantity', 'unit_price', 'revenue']]
    
    fact = fact.rename(columns={'sale_id': 'order_id', 'unit_price': 'price'})
    
    print(f"✅ Created fact_sales: {len(fact)} rows")
    
    return customers, products, dates, fact

def load_data(customers, products, dates, fact):
    """Load data into PostgreSQL tables"""
    
    password = "Hoangbaongoc140906!"
    db_host = os.environ.get('DB_HOST', 'localhost')
    engine = create_engine(f"postgresql://postgres:{password}@{db_host}:5433/data_projects")
    
    print("📥 Recreating tables and loading data...")
   
    customers.to_sql('dim_customer', engine, if_exists='replace', index=False)
    products.to_sql('dim_product', engine, if_exists='replace', index=False)
    dates.to_sql('dim_date', engine, if_exists='replace', index=False)
    fact.to_sql('fact_sales', engine, if_exists='replace', index=False)
    
    logging.info("Data loaded successfully")
    print(f"✅ Loaded all tables to PostgreSQL")

def run_pipeline():
    print("=" * 50)
    print("🏗️ STARTING LARGE DATA WAREHOUSE PIPELINE")
    print("=" * 50)
    
    file_path = 'data/sales_data.csv'
    
    df = extract_data(file_path)
    customers, products, dates, fact = transform_data(df)
    load_data(customers, products, dates, fact)
    
    print("=" * 50)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 50)
    logging.info("Warehouse pipeline executed successfully")

if __name__ == "__main__":
    run_pipeline()
