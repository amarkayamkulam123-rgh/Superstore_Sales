import os
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from clean_data import clean_Superstore

CSV_PATH = Path(__file__).resolve().parent.parent / 'data' / 'Superstore_sales.csv'

load_dotenv()

def get_engine():
    url = (f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
           f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    return create_engine(url)

def load_data():
    engine = get_engine()
    customers, products, orders = clean_Superstore(CSV_PATH)

    # Drop tables in reverse dependency order to avoid FK conflicts
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS orders CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS products CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS customers CASCADE"))
        conn.commit()
    print("Existing tables dropped")

    customers.to_sql('customers', engine, if_exists='append', index=False)
    print("Customers loaded")
    products.to_sql('products', engine, if_exists='append', index=False)
    print("Products loaded")
    orders.to_sql('orders', engine, if_exists='append', index=False)
    print("Orders loaded")

if __name__ == "__main__":
    load_data()
    print("All data loaded to PostgreSQL!")
