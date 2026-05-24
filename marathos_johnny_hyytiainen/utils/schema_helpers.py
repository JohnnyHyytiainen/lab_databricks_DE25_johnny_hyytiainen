import re
# Helper script to avoid DELTA_INVALID_CHARACTERS_IN_COLUMN_NAMES error.


def to_snake_case(name):
    clean_name = re.sub(r"[^a-zA-Z0-9]", "_", name.strip())
    clean_name = re.sub(r"_+", "_", clean_name).casefold()
    return clean_name.rstrip("_")


def rename_columns_to_snake_case(df):
    new_columns = [to_snake_case(col) for col in df.columns]
    return df.toDF(*new_columns)
