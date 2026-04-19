# transform.py


import numpy as np
import pandas as pd


# =========================
# Read Data
# =========================
df = pd.read_csv("data/Superstore_Messy.csv")


# =========================
# Standardize Column Names
# =========================
df.columns = [col.upper().replace(" ", "_").replace("-", "_") for col in df.columns]


# =========================
# Remove Unnecessary Columns
# =========================
if 'COUNTRY' in df.columns:
    df.drop('COUNTRY', axis=1, inplace=True)


# =========================
# Remove Duplicate Rows
# =========================
df.drop_duplicates(inplace=True)


# =========================
# Handle Missing Customer Name
# =========================
df['CUSTOMER_NAME'].fillna('Unknown Customer', inplace=True)


# =========================
# Fill Missing City Using Postal Code
# =========================
df['CITY'] = df['CITY'].fillna(
    df.groupby('POSTAL_CODE')['CITY'].transform('first')
)


# =========================
# Fill Missing Postal Code Using City
# =========================
df['POSTAL_CODE'] = df['POSTAL_CODE'].fillna(
    df.groupby('CITY')['POSTAL_CODE'].transform('first')
)


# =========================
# Fill Remaining Missing City and Postal Code
# =========================
df['CITY'].fillna('Unknown City', inplace=True)
df['POSTAL_CODE'].fillna(-1, inplace=True)


# =========================
# Create Unit Price Column
# =========================
df['UNIT_PRICE'] = df['SALES'] / df['QUANTITY']


# =========================
# Fill Missing Sales Values
# Priority:
# 1. Product Name Average Unit Price
# 2. Sub-Category Average Unit Price
# =========================
product_avg_price = df.groupby('PRODUCT_NAME')['UNIT_PRICE'].transform('mean')
subcategory_avg_price = df.groupby('SUB_CATEGORY')['UNIT_PRICE'].transform('mean')


df['SALES'] = df['SALES'].fillna(
    df['QUANTITY'] * product_avg_price.fillna(subcategory_avg_price)
)


# Ensure Sales is always greater than Profit
mask = (df['PROFIT'].notna()) & (df['SALES'] < df['PROFIT'])
df.loc[mask, 'SALES'] = df.loc[mask, 'PROFIT'] + 10


# =========================
# Create Profit Margin Column
# =========================
df['PROFIT_MARGIN'] = df['PROFIT'] / df['SALES']


# =========================
# Fill Missing Profit Values
# Priority:
# 1. Product Name Average Profit Margin
# 2. Sub-Category Average Profit Margin
# =========================
product_profit_margin = df.groupby('PRODUCT_NAME')['PROFIT_MARGIN'].transform('mean')
subcategory_profit_margin = df.groupby('SUB_CATEGORY')['PROFIT_MARGIN'].transform('mean')


df['PROFIT'] = df['PROFIT'].fillna(
    df['SALES'] * product_profit_margin.fillna(subcategory_profit_margin)
)


# =========================
# Recalculate Derived Columns After Filling Missing Values
# =========================
df['UNIT_PRICE'] = df['SALES'] / df['QUANTITY']
df['PROFIT_MARGIN'] = df['PROFIT'] / df['SALES']


# =========================
# Handle Infinite Values
# =========================
df.replace([np.inf, -np.inf], np.nan, inplace=True)


# =========================
# Convert Date Columns to Datetime
# =========================
df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'], errors='coerce')
df['SHIP_DATE'] = pd.to_datetime(df['SHIP_DATE'], errors='coerce')


# =========================
# Create Shipping Days Column
# =========================
df['SHIPPING_DAYS'] = (df['SHIP_DATE'] - df['ORDER_DATE']).dt.days


# =========================
# Remove Invalid Shipping Days
# =========================
df = df[df['SHIPPING_DAYS'] >= 0]


# =========================
# Standardize Ship Mode Values
# =========================
df['SHIP_MODE'] = df['SHIP_MODE'].replace('unknown', 'Unknown')


# =========================
# Save Final Cleaned Dataset
# =========================
df.to_csv("data/Superstore_Final_Cleaned.csv", index=False)


print("Transformation completed successfully.")
print(df.shape)


