import pandas  as pd
import argparse
import logging
import sys
from pathlib import Path

# ── Logging setup ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── Column rename map (customize as needed) ────────────────────
COLUMN_RENAMES = {
    "name":      "Full Name",
    "age":       "Age",
    "join_date": "Join Date",
    "salary":    "Salary (USD)",
}

def read_csv(input_path: str) -> pd.DataFrame:
    """Read CSV file with error handling."""
    path = Path(input_path)
    if not path.exists():
        logger.error(f"File not found: {input_path}")
        sys.exit(1)
    if path.suffix.lower() != ".csv":
        logger.error(f"Not a CSV file: {input_path}")
        sys.exit(1)

    logger.info(f"Reading file: {input_path}")
    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the dataframe."""

    # 1. Drop fully empty rows
    before = len(df)
    df.dropna(how="all", inplace=True)
    logger.info(f"Removed {before - len(df)} fully empty rows")

    # 2. Fill missing numeric values with column median
    for col in df.select_dtypes(include="number").columns:
        missing = df[col].isna().sum()
        if missing:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            logger.info(f"Filled {missing} missing values in '{col}' with median ({median_val})")

    # 3. Fill missing text values with "Unknown"
    for col in df.select_dtypes(include="object").columns:
        missing = df[col].isna().sum()
        if missing:
            df[col].fillna("Unknown", inplace=True)
            logger.info(f"Filled {missing} missing values in '{col}' with 'Unknown'")

    # 4. Parse date columns
    for col in df.columns:
        if "date" in col.lower():
            original = df[col].copy()
            df[col] = pd.to_datetime(df[col], errors="coerce")
            bad = df[col].isna().sum()
            if bad:
                logger.warning(f"Could not parse {bad} date(s) in '{col}' — set to NaT")

    # 5. Rename columns
    rename_map = {k: v for k, v in COLUMN_RENAMES.items() if k in df.columns}
    if rename_map:
        df.rename(columns=rename_map, inplace=True)
        logger.info(f"Renamed columns: {rename_map}")

    return df

def export_to_excel(df: pd.DataFrame, output_path: str) -> None:
    """Export dataframe to a formatted .xlsx file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")

        # Auto-fit column widths
        ws = writer.sheets["Data"]
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = max_len + 4

    logger.info(f"✅ Saved Excel file: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a cleaned Excel (.xlsx) file"
    )
    parser.add_argument("--input",  "-i", required=True, help="Path to input CSV file")
    parser.add_argument("--output", "-o", default="output.xlsx", help="Path for output .xlsx file")
    args = parser.parse_args()

    df = read_csv(args.input)
    df = clean_data(df)
    export_to_excel(df, args.output)

if __name__ == "__main__":
    main()