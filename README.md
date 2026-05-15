# 📊 CSV → Excel Converter

Convert CSV files to clean, formatted Excel (.xlsx) files using Python.

## Features
- Cleans missing values (fills numeric with median, text with "Unknown")
- Parses date columns automatically
- Renames columns to readable names
- Auto-fits Excel column widths
- CLI flags for input/output paths
- Logging and error messages for bad files

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python converter.py --input data.csv --output result.xlsx
```

## Tech Stack
- Python 3.x
- pandas
- openpyxl# CSV to Excel Converter 
