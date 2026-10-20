
from pathlib import Path
import logging

import pandas as pd


logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "Superstore_Messy.csv"


def extract_data() -> pd.DataFrame:
    """Read the raw Superstore dataset and return a DataFrame."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    if df.empty:
        raise ValueError("The raw dataset is empty.")

    logger.info(
        "Extraction completed: %s rows and %s columns",
        len(df),
        len(df.columns),
    )

    return df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    extracted_df = extract_data()

    print("\nDataset shape:", extracted_df.shape)
    print("\nColumn names:", extracted_df.columns.tolist())
    print("\nMissing values:\n", extracted_df.isnull().sum())
    print("\nFirst five rows:\n", extracted_df.head())
