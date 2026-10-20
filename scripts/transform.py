
from pathlib import Path
import logging

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "Superstore_Final_Cleaned.csv"


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the extracted Superstore dataset."""

    if df.empty:
        raise ValueError("Cannot transform an empty dataset.")

    df = df.copy()
    initial_rows = len(df)

    # Standardize column names.
    df.columns = [
        col.strip().upper().replace(" ", "_").replace("-", "_")
        for col in df.columns
    ]

    # Remove exact duplicate records.
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Check required columns.
    required_columns = [
        "ORDER_ID",
        "ORDER_DATE",
        "SHIP_DATE",
        "PRODUCT_ID",
        "PRODUCT_NAME",
        "SALES",
        "QUANTITY",
        "PROFIT",
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns missing: {missing_columns}"
        )

    # Normalize text fields.
    text_columns = df.select_dtypes(include=["object"]).columns

    for col in text_columns:
        df[col] = df[col].str.strip()

    # Standardize missing categorical values.
    for col in ["CUSTOMER_NAME", "CITY", "SHIP_MODE"]:
        if col in df.columns:
            df[col] = df[col].fillna(
                {
                    "CUSTOMER_NAME": "Unknown Customer",
                    "CITY": "Unknown City",
                    "SHIP_MODE": "Unknown",
                }[col]
            )

    # Preserve missing postal codes explicitly.
    if "POSTAL_CODE" in df.columns:
        df["POSTAL_CODE"] = df["POSTAL_CODE"].astype("string")
        df["POSTAL_CODE"] = df["POSTAL_CODE"].fillna("UNKNOWN")

    # Convert numeric fields safely.
    numeric_columns = [
        "ROW_ID",
        "SALES",
        "QUANTITY",
        "DISCOUNT",
        "PROFIT",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Record missing measures instead of inventing financial values.
    df["SALES_WAS_MISSING"] = df["SALES"].isna()
    df["PROFIT_WAS_MISSING"] = df["PROFIT"].isna()

    # Parse dates using the source's day-first date format.
    for col in ["ORDER_DATE", "SHIP_DATE"]:
        df[col] = pd.to_datetime(
            df[col],
            format="mixed",
            dayfirst=True,
            errors="coerce",
        )

    # Calculate shipping duration without silently dropping records.
    df["SHIPPING_DAYS"] = (
        df["SHIP_DATE"] - df["ORDER_DATE"]
    ).dt.days

    invalid_dates = (
        df["ORDER_DATE"].isna() | df["SHIP_DATE"].isna()
    )

    negative_shipping_days = df["SHIPPING_DAYS"] < 0

    # Invalid durations are flagged for investigation.
    df["INVALID_SHIPPING_DAYS"] = (
        invalid_dates | negative_shipping_days
    )

    # Calculate derived measures only where mathematically valid.
    valid_quantity = df["QUANTITY"].notna() & df["QUANTITY"].ne(0)

    df["UNIT_PRICE"] = (
        df["SALES"] / df["QUANTITY"].where(valid_quantity)
    )

    valid_sales = df["SALES"].notna() & df["SALES"].ne(0)

    df["PROFIT_MARGIN"] = (
        df["PROFIT"] / df["SALES"].where(valid_sales)
    )

    # Replace infinite derived values with missing values.
    derived_columns = ["UNIT_PRICE", "PROFIT_MARGIN"]

    df[derived_columns] = df[derived_columns].replace(
        [np.inf, -np.inf], np.nan
    )

    logger.info("Input rows: %s", initial_rows)
    logger.info("Exact duplicate rows removed: %s", duplicates)
    logger.info("Output rows: %s", len(df))
    logger.info(
        "Rows with missing Sales: %s",
        int(df["SALES"].isna().sum()),
    )
    logger.info(
        "Rows with missing Profit: %s",
        int(df["PROFIT"].isna().sum()),
    )
    logger.info(
        "Rows with invalid shipping dates/durations: %s",
        int(df["INVALID_SHIPPING_DAYS"].sum()),
    )

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    from scripts.extract import extract_data

    cleaned_df = transform_data(extract_data())

    cleaned_df.to_csv(CLEANED_DATA_PATH, index=False)

    logger.info(
        "Cleaned dataset saved to %s",
        CLEANED_DATA_PATH,
    )
