
import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "Superstore_Final_Cleaned.csv"

load_dotenv(PROJECT_ROOT / ".env")


def load_data(df: pd.DataFrame) -> int:
    """Load validated data into PostgreSQL without overwriting an existing table."""
    if df.empty:
        raise ValueError("Cannot load an empty DataFrame.")

    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]
    missing = [key for key in required_vars if not os.getenv(key)]
    if missing:
        raise ValueError(
            f"Missing database configuration: {', '.join(missing)}"
        )

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    engine = create_engine(
        db_url,
        connect_args={"connect_timeout": 5},
    )

    try:
        # Check the connection and whether the target table already exists.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            table_exists = connection.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                          AND table_name = 'superstore_v2'
                    )
                """)
            ).scalar()

        if table_exists:
            raise RuntimeError(
                "Table 'public.superstore_v2' already exists. "
                "No data was loaded or overwritten. "
                "Choose an explicit migration or replacement strategy."
            )

        # Create the table and insert all rows in one transaction.
        with engine.begin() as connection:
            df.to_sql(
                name="superstore_v2",
                con=connection,
                schema="public",
                if_exists="fail",
                index=False,
                chunksize=1000,
                method="multi",
            )

        logger.info(
            "Successfully loaded %s rows into %s.public.superstore_v2",
            len(df),
            os.environ["DB_NAME"],
        )
        return len(df)

    finally:
        engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {DATA_FILE}")

    cleaned_df = pd.read_csv(DATA_FILE)
    cleaned_df.columns = [column.lower() for column in cleaned_df.columns]

    load_data(cleaned_df)
