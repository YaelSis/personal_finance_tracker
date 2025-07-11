
# analysis.py - Personal Finance Tracker Analysis Module
# analysis.py
import pandas as pd


def filter_expenses(df):
    """Handle both cases: with Type column or negative amounts"""
    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()

    if 'type' in df.columns:
        return df[df['type'].str.lower() == 'expense'].copy()
    else:
        return df[df['amount'] < 0].copy()


def analyze_spending_by_category(df):
    df.columns = df.columns.str.lower()  # Normalize columns
    expenses = filter_expenses(df)

    if expenses.empty:
        print("\nNo expenses to analyze.")
        return

    # Ensure amount is numeric and absolute value
    expenses['amount'] = pd.to_numeric(expenses['amount']).abs()

    category_totals = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    print("\n--- Total Spending by Category ---")
    print(category_totals.to_string())


def calculate_average_monthly_spending(df):
    df.columns = df.columns.str.lower()  # Normalize columns
    expenses = filter_expenses(df)

    if expenses.empty:
        print("\nNo expenses data available.")
        return

    # Convert and process dates
    expenses['date'] = pd.to_datetime(expenses['date'])
    expenses['month'] = expenses['date'].dt.to_period('M')

    # Ensure amount is numeric and absolute value
    expenses['amount'] = pd.to_numeric(expenses['amount']).abs()

    monthly_totals = expenses.groupby('month')['amount'].sum()
    average = monthly_totals.mean()
    print("\n--- Average Monthly Spending ---")
    print(f"${average:.2f}")


def show_top_spending_category(df):
    df.columns = df.columns.str.lower()  # Normalize columns
    expenses = filter_expenses(df)

    if expenses.empty:
        print("\nNo expenses data available.")
        return

    # Ensure amount is numeric and absolute value
    expenses['amount'] = pd.to_numeric(expenses['amount']).abs()

    category_totals = expenses.groupby('category')['amount'].sum()
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()
    print("\n--- Top Spending Category ---")
    print(f"{top_category.title()}: ${top_amount:.2f}")

# analysis.py - Personal Finance Tracker Visualization Module
class FinanceVisualizer:
    def __init__(self, data_path=None):
        """Initialize the visualizer with transaction data from CSV file or DataFrame

        Args:
            data_path (str): Path to the CSV file containing transaction data
                            Expected columns: Date, Category, Amount, Type
                            If None, expects df to be set manually
        """
        if data_path:
            self.df = pd.read_csv(data_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])  # Convert string to datetime
        else:
            self.df = pd.DataFrame()

    def show_monthly_expenses(self):
        """Display line chart of monthly expense trends (Expenses only)"""
        # Handle both capitalized and lowercase column names
        date_col = 'Date' if 'Date' in self.df.columns else 'date'
        amount_col = 'Amount' if 'Amount' in self.df.columns else 'amount'
        type_col = 'Type' if 'Type' in self.df.columns else 'type'

        expenses = self.df[self.df[type_col].str.lower() == 'expense'].copy()
        monthly = expenses.groupby(expenses[date_col].dt.to_period('M'))[amount_col].sum()

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
        # Handle both capitalized and lowercase column names
        category_col = 'Category' if 'Category' in self.df.columns else 'category'
        amount_col = 'Amount' if 'Amount' in self.df.columns else 'amount'
        type_col = 'Type' if 'Type' in self.df.columns else 'type'

        expenses = self.df[self.df[type_col].str.lower() == 'expense'].copy()
        category_spending = expenses.groupby(category_col)[amount_col].sum().sort_values()

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
        # Handle both capitalized and lowercase column names
        category_col = 'Category' if 'Category' in self.df.columns else 'category'
        amount_col = 'Amount' if 'Amount' in self.df.columns else 'amount'
        type_col = 'Type' if 'Type' in self.df.columns else 'type'

        expenses = self.df[self.df[type_col].str.lower() == 'expense'].copy()
        category_spending = expenses.groupby(category_col)[amount_col].sum()

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