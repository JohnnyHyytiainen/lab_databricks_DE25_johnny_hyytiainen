import re

# DRY: Delade hjälpfunktioner för kolumnhantering
# Används av: bronze/raw_marathos.py

def to_snake_case(name: str) -> str:
    """Converts a column name to snake_case."""
    clean_name = re.sub(r"[^a-zA-Z0-9]", "_", name.strip())
    clean_name = re.sub(r"_+", "_", clean_name).casefold()
    return clean_name.rstrip("_")

def rename_columns_to_snake_case(df):
    """Changes name on all columns in a DataFrame to snake_case."""
    new_columns = [to_snake_case(col) for col in df.columns]
    return df.toDF(*new_columns)