import pandas as pd


# =========================
# Read Raw Data
# =========================
df = pd.read_csv("data/Superstore_Messy.csv")


# =========================
# Basic Dataset Information
# =========================
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Rows:")
print(df.head())