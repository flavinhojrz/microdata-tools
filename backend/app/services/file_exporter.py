from pathlib import Path

import pandas as pd


CSV_ENCODING = "utf-8-sig"
DEFAULT_CLEANED_FILENAME = "arquivo_limpo.csv"


def dataframe_to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    csv_text = dataframe.to_csv(index=False)
    return csv_text.encode(CSV_ENCODING)


def build_cleaned_filename(original_filename: str) -> str:
    if not original_filename:
        return DEFAULT_CLEANED_FILENAME

    stem = Path(original_filename).stem.strip()

    if not stem:
        return DEFAULT_CLEANED_FILENAME

    return f"{stem}_clean.csv"
