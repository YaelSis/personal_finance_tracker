import pandas as pd
import os

def import_csv(file_path):
    required_columns = {"Date", "Category", "Description", "Amount"}

    try:
        df = pd.read_csv(file_path)

        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Columnas faltantes: {', '.join(missing)}")

        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Validar fechas inválidas
        if df['Date'].isnull().any():
            raise ValueError("Algunas fechas no tienen el formato correcto (YYYY-MM-DD).")

        # Validar valores numéricos en Amount
        if not pd.api.types.is_numeric_dtype(df['Amount']):
            raise ValueError("La columna 'Amount' debe ser numérica.")

        print("✅ Archivo importado exitosamente.")
        return df

    except FileNotFoundError:
        print("❌ Archivo no encontrado. Verifica el nombre o la ruta.")
        return None
    except ValueError as ve:
        print(f"❌ Error de validación: {ve}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def save_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f"✅ Transacciones guardadas exitosamente en '{file_path}'")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")