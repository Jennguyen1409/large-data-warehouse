from datafake import generate_sales
import os

os.makedirs('data', exist_ok=True)

print("Generating 5,000 rows of sales data...")

df = generate_sales(
    n=5000,
    seed=42,          
    missing_rate=0.0,  
    noise_level=0.0,   
    save_to='data/sales_data.csv'
)

print(f"Generated {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print(f"Saved to data/sales_data.csv")
print("\n First 5 rows:")
print(df.head())
