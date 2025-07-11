import pandas as pd

# We have to filter for expenses only
def filter_expenses(df):
    if "Type" in df.columns:
        return df[df["Type"].str.lower() == "expense"].copy()
    else:
        # Fallback if theres no type column, it'll use negative values
        return df[df['Amount'] < 0].copy()

# Total expenses per category
def analyze_spending_by_category(df):
    expenses = filter_expenses(df)
    if expenses.empty:
        print("\nNo expenses to analyze.")
        return
    category_totals = expenses.groupby('Category')['Amount'].sum().abs() # we grouo the categories and their amounts
    print("\n--- Total Spending by Category ---")
    print(category_totals.sort_values(ascending=False))

# Monthly average expenses
def calculate_average_monthly_spending(df):
    df['Date'] = pd.to_datetime(df['Date'])
    expenses = filter_expenses(df)
    if expenses.empty:
        print("\nNo expenses data to calculate monthly average expenses.")
        return
    expenses['Month'] = expenses['Date'].dt.to_period('M')
    monthly_totals = expenses.groupby('Month')['Amount'].sum().abs()
    average = monthly_totals.mean()
    print("\n--- Average Monthly Spending ---")
    print(round(average, 2))

# Category with the biggest expenses
def show_top_spending_category(df):
    expenses = filter_expenses(df)
    if expenses.empty:
        print("\nNo expenses to identify main category.")
        return
    category_totals = expenses.groupby('Category')['Amount'].sum().abs()
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()
    print("\n--- Top Spending Category (Expenses Only) ---")
    print(f"{top_category} with {top_amount:.2f} total spending.")

#============
#=========================RENE=======================================

# analysis.py - Personal Finance Tracker Visualization Module
import pandas as pd
import matplotlib.pyplot as plt


class FinanceVisualizer:
    def __init__(self, data_path='sampledata.csv'):
        """Initialize the visualizer with transaction data from CSV file

        Args:
            data_path (str): Path to the CSV file containing transaction data
                            Expected columns: Date, Category, Amount, Type
        """
        self.df = pd.read_csv(data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])  # Convert string to datetime

    def show_monthly_expenses(self):
        """Display line chart of monthly expense trends (Expenses only)"""
        expenses = self.df[self.df['Type'] == 'Expense'].copy()
        monthly = expenses.groupby(expenses['Date'].dt.to_period('M'))['Amount'].sum()

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

    def show_spending_by_category(self):
        """Display horizontal bar chart of spending by category (Expenses only)"""
        expenses = self.df[self.df['Type'] == 'Expense'].copy()
        category_spending = expenses.groupby('Category')['Amount'].sum().sort_values()

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
        """Display pie chart of spending distribution (Expenses only)"""
        expenses = self.df[self.df['Type'] == 'Expense'].copy()
        category_spending = expenses.groupby('Category')['Amount'].sum()

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


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("✅ Loading transaction data from sampledata.csv...")
    visualizer = FinanceVisualizer()  # Uses default CSV path
    visualizer.show_monthly_expenses()
    visualizer.show_spending_by_category()
    visualizer.show_spending_distribution()


