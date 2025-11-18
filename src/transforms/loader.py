import pandas as pd
from pathlib import Path

def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    path (str): The file path to the CSV file.
    **kwargs: Additional keyword arguments to pass to pd.read_csv().

    Returns:
    pd.DataFrame: The loaded DataFrame.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path, **kwargs)