import pandas as pd
import os

def import_csv(file_path):
    required_columns = {"Date", "Category", "Description", "Amount"}

    try:
        df = pd.read_csv(file_path)

        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Validar fechas inválidas
        if df['Date'].isnull().any():
            raise ValueError("Some dates have wrong format (YYYY-MM-DD).")

        # Validar valores numéricos en Amount
        if not pd.api.types.is_numeric_dtype(df['Amount']):
            raise ValueError("Column 'Amount'  must be numeric.")

        print(" File successfully imported.")
        return df

    except FileNotFoundError:
        print(" File not found.")
        return None
    except ValueError as ve:
        print(f" Validation error: {ve}")
        return None
    except Exception as e:
        print(f" Unexpected error: {e}")
        return None

def save_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f" Transaction saved successfully in '{file_path}'")
    except Exception as e:
        print(f" Error saving the file: {e}")