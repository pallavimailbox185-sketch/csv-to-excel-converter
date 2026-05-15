import pandas as pd
import argparse
import logging
import os
from datetime import datetime

# ─── Logging Setup ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def clean_data(df, date_columns=None, rename_map=None):
    """Clean and normalize the DataFrame."""

    # 1. Fill missing values
    df.fillna("N/A", inplace=True)
    logging.info("Filled missing values with 'N/A'")

    # 2. Parse date columns if provided
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                logging.info(f"Parsed dates in column: {col}")

    # 3. Rename columns if mapping provided
    if rename_map:
        df.rename(columns=rename_map, inplace=True)
        logging.info(f"Renamed columns: {rename_map}")

    return df

def csv_to_excel(input_file, output_path=None):
    """Main conversion function."""

    # Validate input file
    if not os.path.exists(input_file):
        logging.error(f"File not found: {input_file}")
        raise FileNotFoundError(f"No such file: {input_file}")

    if not input_file.endswith(".csv"):
        logging.error("Input file must be a .csv file")
        raise ValueError("Only .csv files are supported")

    # Read CSV
    logging.info(f"Reading CSV: {input_file}")
    df = pd.read_csv(input_file)

    # Clean data
    df = clean_data(df)

    # Set output path
    if not output_path:
        base = os.path.splitext(input_file)[0]
        output_path = f"{base}_converted.xlsx"

    # Export to Excel
    df.to_excel(output_path, index=False, engine='openpyxl')
    logging.info(f"✅ Saved Excel file to: {output_path}")
    print(f"\n✅ Done! Excel file saved at: {output_path}")

# ─── CLI ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert CSV to Excel (.xlsx)"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input CSV file"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path for output .xlsx file (optional)"
    )
    args = parser.parse_args()

    csv_to_excel(args.input, args.output)