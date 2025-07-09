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

