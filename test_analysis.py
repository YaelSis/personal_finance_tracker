"""
import pandas as pd


from analysis import (
    analyze_spending_by_category,
    calculate_average_monthly_spending,
    show_top_spending_category
)

df = pd.read_csv("sampledata.csv")  # Asegúrate de tener este archivo en la raíz

analyze_spending_by_category(df)
calculate_average_monthly_spending(df)
show_top_spending_category(df)


from analysis import (
    analyze_spending_by_category,
    calculate_average_monthly_spending,
    show_top_spending_category
)

# Cargar el CSV con los datos
try:
    df = pd.read_csv("sampledata.csv")

    # Verificar que las columnas necesarias existan
    required_columns = {'Date', 'Category', 'Description', 'Amount'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Faltan columnas requeridas: {required_columns - set(df.columns)}")

    # Ejecutar las funciones de análisis
    analyze_spending_by_category(df)
    calculate_average_monthly_spending(df)
    show_top_spending_category(df)

except FileNotFoundError:
    print("Error: El archivo 'sampledata.csv' no se encuentra.")
except Exception as e:
    print(f"Error al procesar los datos: {e}")
"""


# Modify the filter_expenses function (around line 3)
def filter_expenses(df):
    # Make column names case-insensitive
    amount_col = 'Amount' if 'Amount' in df.columns else 'amount'

    if "Type" in df.columns:
        return df[df["Type"].str.lower() == "expense"].copy()
    else:
        # Fallback if there's no type column, use negative values
        return df[df[amount_col] < 0].copy()


# Modify analyze_spending_by_category (around line 10)
def analyze_spending_by_category(df):
    expenses = filter_expenses(df)
    if expenses.empty:
        print("\nNo expenses to analyze.")
        return

    # Make column names case-insensitive
    category_col = 'Category' if 'Category' in df.columns else 'category'
    amount_col = 'Amount' if 'Amount' in df.columns else 'amount'

    category_totals = expenses.groupby(category_col)[amount_col].sum().abs()
    print("\n--- Total Spending by Category ---")
    print(category_totals.sort_values(ascending=False))


# Modify calculate_average_monthly_spending (around line 19)
def calculate_average_monthly_spending(df):
    # Make column names case-insensitive
    date_col = 'Date' if 'Date' in df.columns else 'date'
    amount_col = 'Amount' if 'Amount' in df.columns else 'amount'

    df[date_col] = pd.to_datetime(df[date_col])
    expenses = filter_expenses(df)
    if expenses.empty:
        print("\nNo expenses data to calculate monthly average expenses.")
        return

    expenses['Month'] = expenses[date_col].dt.to_period('M')
    monthly_totals = expenses.groupby('Month')[amount_col].sum().abs()
    average = monthly_totals.mean()
    print("\n--- Average Monthly Spending ---")
    print(round(average, 2))


# Modify show_top_spending_category (around line 30)
def show_top_spending_category(df):
    expenses = filter_expenses(df)
    if expenses.empty:
        print("\nNo expenses to identify main category.")
        return

    # Make column names case-insensitive
    category_col = 'Category' if 'Category' in df.columns else 'category'
    amount_col = 'Amount' if 'Amount' in df.columns else 'amount'

    category_totals = expenses.groupby(category_col)[amount_col].sum().abs()
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()
    print("\n--- Top Spending Category ---")
    print(f"{top_category} with {top_amount:.2f} total spending.")


# Modify the FinanceVisualizer class (around line 45)
class FinanceVisualizer:
    def __init__(self, data_path=None):
        """Initialize with optional DataFrame or CSV path"""
        if data_path:
            self.df = pd.read_csv(data_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
        else:
            self.df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Type'])

    def show_monthly_expenses(self):
        """Handle both capitalized and lowercase column names"""
        date_col = 'Date' if 'Date' in self.df.columns else 'date'
        amount_col = 'Amount' if 'Amount' in self.df.columns else 'amount'
        type_col = 'Type' if 'Type' in self.df.columns else 'type'

        expenses = self.df[self.df[type_col] == 'Expense'].copy()
        monthly = expenses.groupby(expenses[date_col].dt.to_period('M'))[amount_col].sum()

        # Rest of the visualization code remains the same...
        plt.figure(figsize=(10, 5))
        monthly.plot(
            kind='line',
            title='Monthly Expenses Trend',
            marker='o',
            color='teal',
            linewidth=2
        )
        plt.ylabel('Amount ($)')
        plt.xlabel('Month')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()

    # Make similar changes to show_spending_by_category and show_spending_distribution
    def show_spending_by_category(self):
        """Handle both capitalized and lowercase column names"""
        category_col = 'Category' if 'Category' in self.df.columns else 'category'
        amount_col = 'Amount' if 'Amount' in self.df.columns else 'amount'
        type_col = 'Type' if 'Type' in self.df.columns else 'type'

        expenses = self.df[self.df[type_col] == 'Expense'].copy()
        category_spending = expenses.groupby(category_col)[amount_col].sum().sort_values()

        # Rest of the visualization code remains the same...
        plt.figure(figsize=(10, 5))
        category_spending.plot(
            kind='barh',
            title='Spending by Category',
            color='skyblue',
            edgecolor='black'
        )
        plt.xlabel('Amount ($)')
        plt.tight_layout()
        plt.show()

    def show_spending_distribution(self):
        """Handle both capitalized and lowercase column names"""
        category_col = 'Category' if 'Category' in self.df.columns else 'category'
        amount_col = 'Amount' if 'Amount' in self.df.columns else 'amount'
        type_col = 'Type' if 'Type' in self.df.columns else 'type'

        expenses = self.df[self.df[type_col] == 'Expense'].copy()
        category_spending = expenses.groupby(category_col)[amount_col].sum()

        # Rest of the visualization code remains the same...
        plt.figure(figsize=(8, 8))
        category_spending.plot(
            kind='pie',
            title='Spending Distribution',
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            colormap='Pastel2'
        )
        plt.ylabel('')
        plt.show()