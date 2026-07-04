# 📊 Superstore Sales BI Dashboard

An end-to-end Business Intelligence project that transforms raw Superstore sales data into actionable insights through a **Python ETL pipeline**, **PostgreSQL data warehouse**, and an interactive **Power BI dashboard**.

---

## 🏗️ Project Architecture

```
Raw CSV Data ──▶ Python ETL (Clean & Transform) ──▶ PostgreSQL Database ──▶ Power BI Dashboard
```

```
superstore_bi/
│
├── 📁 data/
│   └── Superstore_sales.csv          # Raw source data (9,994 transactions)
│
├── 📁 scripts/
│   ├── clean_data.py                 # Data cleaning & transformation logic
│   └── load_to_postgres.py           # Database loading script
│
├── 📁 sql/
│   └── create_tables.sql             # PostgreSQL table schema definitions
│
├── 📊 Superstore_Sales_Dashboard.pbix  # Power BI interactive dashboard
├── 🎨 123.json                       # Power BI theme – Modern Dark Dashboard
├── 🎨 456.json                       # Power BI theme – HR Workforce Analytics (Light)
├── 📋 requirements.txt               # Python dependencies
├── 🔒 .env                           # Database connection credentials (not committed)
└── 📖 README.md                      # This file
```

---

## 📦 Dataset Overview

**Source**: [Kaggle – Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

The dataset contains **9,994 retail transaction records** from a US-based superstore spanning **2016–2019**, with the following fields:

| Field          | Description                              |
|----------------|------------------------------------------|
| `Order ID`     | Unique identifier for each order         |
| `Order Date`   | Date the order was placed                |
| `Ship Date`    | Date the order was shipped               |
| `Ship Mode`    | Shipping method (Standard, Express, etc.)|
| `Customer ID`  | Unique customer identifier               |
| `Customer Name`| Full name of the customer                |
| `Segment`      | Customer segment (Consumer, Corporate, Home Office) |
| `Country`      | Country of the customer                  |
| `City / State / Region` | Geographic details              |
| `Product ID`   | Unique product identifier                |
| `Category`     | Product category (Furniture, Office Supplies, Technology) |
| `Sub-Category` | Product sub-category                     |
| `Product Name` | Full product name                        |
| `Sales`        | Total sales amount (USD)                 |
| `Quantity`     | Number of units sold                     |
| `Discount`     | Discount applied (0–1)                   |
| `Profit`       | Profit earned from the transaction       |

---

## ⚙️ ETL Pipeline

### 1. Data Cleaning (`scripts/clean_data.py`)

The cleaning script performs the following transformations:

- **Column Normalization** — Converts all column headers to lowercase with underscores
- **Date Parsing** — Converts `order_date` and `ship_date` to proper datetime objects
- **Deduplication** — Removes duplicate rows based on `order_id` + `product_id`
- **Feature Engineering**:
  - `profit_margin` — Calculated as `profit / sales` (rounded to 4 decimal places)
  - `days_to_ship` — Number of days between order and shipment
- **Data Normalization** — Splits the flat CSV into 3 relational tables:
  - **Customers** — `customer_id`, `customer_name`, `segment`, `country`, `city`, `state`, `region`
  - **Products** — `product_id`, `product_name`, `category`, `sub_category`
  - **Orders** — `order_id`, `order_date`, `ship_date`, `ship_mode`, `customer_id`, `product_id`, `sales`, `quantity`, `discount`, `profit`

### 2. Database Loading (`scripts/load_to_postgres.py`)

- Connects to PostgreSQL using credentials from the `.env` file
- Drops existing tables (in reverse dependency order to handle foreign keys)
- Loads the cleaned **Customers**, **Products**, and **Orders** DataFrames into PostgreSQL using SQLAlchemy

---

## 🗄️ Database Schema

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    customers      │     │      orders       │     │    products       │
├──────────────────┤     ├──────────────────┤     ├──────────────────┤
│ customer_id (PK) │◄────│ customer_id (FK) │     │ product_id (PK)  │
│ customer_name    │     │ product_id (FK)  │────►│ product_name     │
│ segment          │     │ order_id         │     │ category         │
│ country          │     │ order_date       │     │ sub_category     │
│ city             │     │ ship_date        │     └──────────────────┘
│ state            │     │ ship_mode        │
│ region           │     │ sales            │
└──────────────────┘     │ quantity         │
                         │ discount         │
                         │ profit           │
                         └──────────────────┘
```

---

## 🎨 Power BI Themes

Two pre-built Power BI theme files are included for quick styling:

| File       | Theme Name               | Style      | Primary Colors                     |
|------------|--------------------------|------------|-------------------------------------|
| `123.json` | Modern Dark Dashboard    | 🌑 Dark   | `#1E1E2E` background, `#89B4FA` accent, Catppuccin palette |
| `456.json` | HR Workforce Analytics   | 🌕 Light  | `#F6F2FF` background, `#8B5CF6` accent, Purple palette     |

**To apply a theme in Power BI Desktop:**
1. Open your `.pbix` file
2. Go to **View → Themes → Browse for themes**
3. Select either `123.json` or `456.json`
4. Click **Open** — the theme is applied instantly

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **PostgreSQL** installed and running
- **Power BI Desktop** (Windows only)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/superstore_bi.git
cd superstore_bi
```

### 2. Install Python Dependencies

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

### 3. Configure Database Connection

Create or update the `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=superstore_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Create the PostgreSQL Database

```sql
CREATE DATABASE superstore_db;
```

### 5. Run the ETL Pipeline

```bash
cd scripts
python load_to_postgres.py
```

This will:
- Read the raw CSV from `data/Superstore_sales.csv`
- Clean and transform the data
- Load it into 3 PostgreSQL tables (`customers`, `products`, `orders`)

### 6. Open the Power BI Dashboard

- Open `Superstore_Sales_Dashboard.pbix` in **Power BI Desktop**
- Update the data source connection to point to your PostgreSQL instance
- Click **Refresh** to pull in the latest data
- Optionally apply a theme from `123.json` or `456.json`

---

## 🛠️ Tech Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| **Data Source**   | CSV (Kaggle Superstore Dataset)    |
| **ETL**          | Python, Pandas                     |
| **Database**     | PostgreSQL                         |
| **ORM / Driver** | SQLAlchemy, psycopg2               |
| **Config**       | python-dotenv (`.env` file)        |
| **Visualization**| Power BI Desktop                   |
| **Theming**      | Power BI JSON Theme Files          |

---

## 📌 Key Metrics Tracked

The dashboard provides insights into:

- 💰 **Total Sales & Profit** — Overall revenue and profitability
- 📈 **Sales Trends** — Monthly/yearly sales patterns
- 🏷️ **Category Performance** — Sales breakdown by Furniture, Office Supplies, Technology
- 🚚 **Shipping Analysis** — Average days to ship, ship mode distribution
- 🌎 **Geographic Analysis** — Sales by region, state, and city
- 👥 **Customer Segments** — Consumer vs. Corporate vs. Home Office
- 📊 **Profit Margins** — Profitability analysis across products and categories
- 🔖 **Discount Impact** — Correlation between discounts and profit

---

## 📝 License

This project is for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- Dataset sourced from [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- Power BI themes inspired by [Catppuccin](https://catppuccin.com/) color palette
