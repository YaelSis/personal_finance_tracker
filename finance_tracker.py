import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class FinanceTracker:
    def __init__(self):
        self.df = pd.DataFrame(columns=['date', 'category', 'description', 'amount', 'type'])

    def import_csv(self, file_path):
        try:
            # Read CSV file
            df = pd.read_csv(file_path)

            # Normalize column names to lowercase
            df.columns = df.columns.str.lower()

            # Check for required columns
            required_cols = ['date', 'category', 'amount']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns: {', '.join(missing)}")

            # Convert date from DD/MM/YYYY to datetime
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

            # Check for invalid dates
            if df['date'].isnull().any():
                invalid_count = df['date'].isnull().sum()
                raise ValueError(f"Found {invalid_count} invalid date(s). Please use DD/MM/YYYY format.")

            # Ensure amount is numeric
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

            # Handle type column (add if missing, capitalize if present)
            if 'type' not in df.columns:
                df['type'] = 'Expense'
            else:
                df['type'] = df['type'].str.capitalize()
                df['type'] = df['type'].fillna('Expense')

            # Keep only the columns we want
            self.df = df[['date', 'category', 'description', 'amount', 'type']].copy()
            return True, "File imported successfully"

        except Exception as e:
            return False, f"Error importing file: {str(e)}"

    def view_transactions(self, start_date=None, end_date=None):
        if self.df.empty:
            return "No transactions available"

        if start_date and end_date:
            try:
                start = pd.to_datetime(start_date, dayfirst=True)
                end = pd.to_datetime(end_date, dayfirst=True)
                filtered = self.df[(self.df['date'] >= start) & (self.df['date'] <= end)]
                return filtered if not filtered.empty else "No transactions in date range"
            except:
                return "Invalid date format (use DD/MM/YYYY)"
        return self.df

    def add_transaction(self, date, category, description, amount, transaction_type='Expense'):
        try:
            new_tx = {
                'date': pd.to_datetime(date, dayfirst=True),
                'category': category,
                'description': description,
                'amount': float(amount),
                'type': transaction_type.capitalize()
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_tx])], ignore_index=True)
            return True, "Transaction added successfully"
        except Exception as e:
            return False, f"Error adding transaction: {str(e)}"

    def edit_transaction(self, index, date=None, category=None, description=None, amount=None, transaction_type=None):
        try:
            if index not in self.df.index:
                return False, "Invalid transaction index"

            if date:
                self.df.at[index, 'date'] = pd.to_datetime(date, dayfirst=True)
            if category:
                self.df.at[index, 'category'] = category
            if description:
                self.df.at[index, 'description'] = description
            if amount:
                self.df.at[index, 'amount'] = float(amount)
            if transaction_type:
                self.df.at[index, 'type'] = transaction_type.capitalize()

            return True, "Transaction updated successfully"
        except Exception as e:
            return False, f"Error updating transaction: {str(e)}"

    def delete_transaction(self, index):
        try:
            if index not in self.df.index:
                return False, "Invalid transaction index"
            self.df = self.df.drop(index).reset_index(drop=True)
            return True, "Transaction deleted successfully"
        except Exception as e:
            return False, f"Error deleting transaction: {str(e)}"

    def save_to_csv(self, file_path):
        try:
            self.df.to_csv(file_path, index=False)
            return True, f"Transactions saved to {file_path}"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"

    # Analysis Functions
    def analyze_spending_by_category(self):
        if self.df.empty:
            return "No transactions to analyze"

        expenses = self.df[self.df['type'] == 'Expense'].copy()
        if expenses.empty:
            return "No expense transactions found"

        expenses['amount'] = expenses['amount'].abs()
        category_totals = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
        return category_totals

    def calculate_average_monthly_spending(self):
        if self.df.empty:
            return "No transactions to analyze"

        expenses = self.df[self.df['type'] == 'Expense'].copy()
        if expenses.empty:
            return "No expense transactions found"

        expenses['amount'] = expenses['amount'].abs()
        expenses['month'] = expenses['date'].dt.to_period('M')
        monthly_totals = expenses.groupby('month')['amount'].sum()
        return round(monthly_totals.mean(), 2)

    def show_top_spending_category(self):
        if self.df.empty:
            return "No transactions to analyze"

        expenses = self.df[self.df['type'] == 'Expense'].copy()
        if expenses.empty:
            return "No expense transactions found"

        expenses['amount'] = expenses['amount'].abs()
        category_totals = expenses.groupby('category')['amount'].sum()
        top_category = category_totals.idxmax()
        top_amount = category_totals.max()
        return f"{top_category}: ${top_amount:.2f}"

    # Visualization Functions
    def show_monthly_expenses(self):
        if self.df.empty:
            print("No transactions to visualize")
            return

        expenses = self.df[self.df['type'] == 'Expense'].copy()
        if expenses.empty:
            print("No expense transactions to visualize")
            return

        expenses['amount'] = expenses['amount'].abs()
        expenses['month'] = expenses['date'].dt.to_period('M')
        monthly = expenses.groupby('month')['amount'].sum()

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
        plt.tight_layout()
        plt.show()

    def show_spending_by_category(self):
        if self.df.empty:
            print("No transactions to visualize")
            return

        expenses = self.df[self.df['type'] == 'Expense'].copy()
        if expenses.empty:
            print("No expense transactions to visualize")
            return

        expenses['amount'] = expenses['amount'].abs()
        category_spending = expenses.groupby('category')['amount'].sum().sort_values()

        plt.figure(figsize=(10, 6))
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
        if self.df.empty:
            print("No transactions to visualize")
            return

        expenses = self.df[self.df['type'] == 'Expense'].copy()
        if expenses.empty:
            print("No expense transactions to visualize")
            return

        expenses['amount'] = expenses['amount'].abs()
        category_spending = expenses.groupby('category')['amount'].sum()

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
        plt.tight_layout()
        plt.show()