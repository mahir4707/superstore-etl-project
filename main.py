
import logging
import sys
from pathlib import Path
from scripts.load import load_data

from scripts.extract import extract_data
from scripts.transform import transform_data


PROJECT_ROOT = Path(__file__).resolve().parent
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "Superstore_Final_Cleaned.csv"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
             LOG_DIR / "pipeline.log",
             encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger("superstore_etl")


def validate_data(df):
    """Run essential checks before the data reaches the loading stage."""

    if df.empty:
        raise ValueError("Validation failed: dataset is empty.")

    required_columns = [
        "ORDER_ID",
        "PRODUCT_ID",
        "ORDER_DATE",
        "SHIP_DATE",
        "SALES",
        "PROFIT",
        "QUANTITY",
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Validation failed: missing columns {missing_columns}"
        )

    if df.duplicated().any():
        raise ValueError("Validation failed: duplicate rows remain.")

    if df["ORDER_ID"].isna().any():
        raise ValueError("Validation failed: missing order IDs.")

    if df["PRODUCT_ID"].isna().any():
        raise ValueError("Validation failed: missing product IDs.")

    logger.info("Validation passed.")
    logger.info("Rows ready for loading: %s", len(df))
    logger.info("Columns ready for loading: %s", len(df.columns))
    logger.info(
        "Missing Sales values: %s",
        int(df["SALES"].isna().sum()),
    )
    logger.info(
        "Missing Profit values: %s",
        int(df["PROFIT"].isna().sum()),
    )
    logger.info(
        "Invalid shipping records flagged: %s",
        int(df["INVALID_SHIPPING_DAYS"].sum()),
    )



def main():
    logger.info("===== SUPERSTORE ETL PIPELINE STARTED =====")

    try:
        logger.info("Stage 1: Extract")
        raw_df = extract_data()

        logger.info("Stage 2: Transform")
        cleaned_df = transform_data(raw_df)

        logger.info("Stage 3: Validate")
        validate_data(cleaned_df)

        logger.info("Stage 4: Save cleaned dataset")
        cleaned_df.to_csv(CLEANED_DATA_PATH, index=False)
        logger.info("Cleaned dataset saved to %s", CLEANED_DATA_PATH)

        logger.info("Stage 5: Load into PostgreSQL")
        rows_loaded = load_data(cleaned_df)
        logger.info("Rows loaded into PostgreSQL: %s", rows_loaded)

        logger.info("===== PIPELINE COMPLETED SUCCESSFULLY =====")

    except Exception:
        logger.exception("ETL pipeline failed.")
        raise


if __name__ == "__main__":
    main()

