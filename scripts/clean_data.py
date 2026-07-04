import pandas as pd

def clean_Superstore(filepath):
    df = pd.read_csv(filepath, encoding='windows-1252')

    df.columns = df.columns.str.lower().str.replace(r'[ -]', '_', regex=True)

    df['order_date'] = pd.to_datetime(df['order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'])

    df.drop_duplicates(subset=['order_id', 'product_id'], inplace=True)

    df['profit_margin'] = (df['profit'] / df['sales'].replace(0, pd.NA)).round(4)
    df['days_to_ship'] = (df['ship_date'] - df['order_date']).dt.days

    customers = df[
        ['customer_id', 'customer_name', 'segment',
         'country', 'city', 'state', 'region']
    ].drop_duplicates()

    products = df[
        ['product_id', 'product_name',
         'category', 'sub_category']
    ].drop_duplicates()

    orders = df[
        ['order_id', 'order_date', 'ship_date', 'ship_mode',
         'customer_id', 'product_id', 'sales',
         'quantity', 'discount', 'profit']
    ].drop_duplicates(subset=['order_id', 'product_id'])

    return customers, products, orders


if __name__ == "__main__":
    c, p, o = clean_Superstore('D:\\superstore_bi\\data\\Superstore_sales.csv')

    print(f"Customers: {len(c)}")
    print(f"Products: {len(p)}")
    print(f"Orders: {len(o)}")