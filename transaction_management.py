import pandas as pd
from datetime import datetime

# Create an empty DataFrame with the required columns
data_columns = ['date', 'category', 'description', 'amount']
df = pd.DataFrame(columns=data_columns)

# Function to view all transactions or filter them by date range
def view_transactions(start_date=None, end_date=None):
    """
    Shows all transactions or filters them by date range.
    """
    if df.empty:
        print("There are no recorded transactions.")
        return

    if start_date and end_date:
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            filtered = df[(df['date'] >= start) & (df['date'] <= end)]
            print(filtered)
        except:
            print("Invalid date format. Use YYYY-MM-DD.")
    else:
        print(df)

# Function to add a new transaction
def add_transaction():
    """
    Asks the user for details and adds a new transaction to the DataFrame.
    """
    try:
        date = input("Date (YYYY-MM-DD): ")
        category = input("Category: ")
        description = input("Description: ")
        amount = float(input("Amount: "))

        # Validate date format
        pd.to_datetime(date)  # Will raise error if invalid

        new_tx = {'date': date, 'category': category, 'description': description, 'amount': amount}
        global df
        df = pd.concat([df, pd.DataFrame([new_tx])], ignore_index=True)
        print("Transaction successfully added.")
    except Exception as e:
        print("Error adding transaction:", e)

# Function to edit a transaction by index
def edit_transaction():
    """
    Lets the user update a transaction using its index.
    """
    print(df)
    try:
        idx = int(input("Index of the transaction to edit: "))
        if idx not in df.index:
            print("Invalid index.")
            return

        print("Leave blank if you don't want to change a field.")
        new_date = input("New date (YYYY-MM-DD): ")
        new_cat = input("New category: ")
        new_desc = input("New description: ")
        new_amount = input("New amount: ")

        if new_date:
            df.at[idx, 'date'] = new_date
        if new_cat:
            df.at[idx, 'category'] = new_cat
        if new_desc:
            df.at[idx, 'description'] = new_desc
        if new_amount:
            df.at[idx, 'amount'] = float(new_amount)

        print("Transaction updated.")
    except Exception as e:
        print("Error editing transaction:", e)

# Function to delete a transaction by index
def delete_transaction():
    """
    Deletes a transaction from the DataFrame using its index.
    """
    print(df)
    try:
        idx = int(input("Index of the transaction to delete: "))
        if idx not in df.index:
            print("Invalid index.")
            return
        global df
        df = df.drop(index=idx).reset_index(drop=True)
        print("Transaction deleted.")
    except Exception as e:
        print("Error deleting transaction:", e)

#Helper function to return the current DataFrame
def get_transactions():
    return df
