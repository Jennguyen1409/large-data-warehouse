# ============================================
# PROJECT 6: Generate Large Synthetic Sales Data
# ============================================

from datafake import generate_sales
import os

# Create data folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# Generate 5,000 rows of sales data
print("📊 Generating 5,000 rows of sales data...")

df = generate_sales(
    n=5000,
    seed=42,           # Same seed = same data every time
    missing_rate=0.0,  # No missing values
    noise_level=0.0,   # No noise
    save_to='data/sales_data.csv'
)

print(f"✅ Generated {len(df)} rows")
print(f"✅ Columns: {list(df.columns)}")
print(f"✅ Saved to data/sales_data.csv")
print("\n📋 First 5 rows:")
print(df.head())