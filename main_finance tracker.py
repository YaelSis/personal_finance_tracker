from finance_tracker import FinanceTracker
import pandas as pd


def display_transactions(transactions):
    """Display transactions in a clean format"""
    if isinstance(transactions, str):
        print(transactions)
    else:
        print(transactions.to_string(index=False))


def main():
    tracker = FinanceTracker()

    while True:
        print("\n=== Personal Finance Tracker ===")
        print("0. Import CSV File")
        print("1. View All Transactions")
        print("2. View Transactions by Date Range")
        print("3. Add a Transaction")
        print("4. Edit a Transaction")
        print("5. Delete a Transaction")
        print("6. Analyze Spending by Category")
        print("7. Calculate Average Monthly Spending")
        print("8. Show Top Spending Category")
        print("9. Visualize Spending (Charts)")
        print("10. Save Transactions to CSV")
        print("11. Exit")

        choice = input("\nChoose an option (0-11): ").strip()

        # Option 0: Import CSV
        if choice == '0':
            path = input("Enter CSV file path: ").strip('"\' ')
            if not path:
                print("No file path provided!")
                continue

            success, message = tracker.import_csv(path)
            print(message)
            if success:
                print("\nFirst 5 transactions:")
                display_transactions(tracker.view_transactions().head(5))

        # Option 1: View All Transactions
        elif choice == '1':
            print("\n--- All Transactions ---")
            display_transactions(tracker.view_transactions())

        # Option 2: View by Date Range
        elif choice == '2':
            print("Enter dates in DD/MM/YYYY format")
            start = input("Start date: ").strip()
            end = input("End date: ").strip()
            print("\n--- Filtered Transactions ---")
            display_transactions(tracker.view_transactions(start, end))

        # Option 3: Add Transaction
        elif choice == '3':
            print("\nEnter transaction details:")
            date = input("Date (DD/MM/YYYY): ").strip()
            category = input("Category: ").strip()
            description = input("Description: ").strip()
            amount = input("Amount: ").strip()
            transaction_type = input("Type (Income/Expense): ").strip().capitalize()

            success, message = tracker.add_transaction(date, category, description, amount, transaction_type)
            print(message)

        # Option 4: Edit Transaction
        elif choice == '4':
            print("\nCurrent transactions:")
            display_transactions(tracker.view_transactions())

            try:
                index = int(input("\nEnter transaction number to edit: ").strip())
                current = tracker.view_transactions().iloc[index]

                print("\nCurrent transaction details:")
                print(current.to_string())

                print("\nEnter new values (leave blank to keep current):")
                new_date = input(f"Date [{current['Date'].strftime('%d/%m/%Y')}]: ").strip()
                new_category = input(f"Category [{current['Category']}]: ").strip()
                new_description = input(f"Description [{current['Description']}]: ").strip()
                new_amount = input(f"Amount [{current['Amount']}]: ").strip()
                new_type = input(f"Type [{current['Type']}]: ").strip().capitalize()

                success, message = tracker.edit_transaction(
                    index,
                    new_date if new_date else None,
                    new_category if new_category else None,
                    new_description if new_description else None,
                    new_amount if new_amount else None,
                    new_type if new_type else None
                )
                print(message)

            except Exception as e:
                print(f"Error: {str(e)}")

        # Option 5: Delete Transaction
        elif choice == '5':
            print("\nCurrent transactions:")
            display_transactions(tracker.view_transactions())

            try:
                index = int(input("\nEnter transaction number to delete: ").strip())
                success, message = tracker.delete_transaction(index)
                print(message)
            except:
                print("Invalid transaction number!")

        # Option 6: Analyze by Category
        elif choice == '6':
            result = tracker.analyze_spending_by_category()
            print("\n--- Spending by Category ---")
            print(result if isinstance(result, str) else result.to_string())

        # Option 7: Average Monthly Spending
        elif choice == '7':
            result = tracker.calculate_average_monthly_spending()
            print("\n--- Average Monthly Spending ---")
            print(f"${result}")

        # Option 8: Top Spending Category
        elif choice == '8':
            result = tracker.show_top_spending_category()
            print("\n--- Top Spending Category ---")
            print(result)

        # Option 9: Visualizations
        elif choice == '9':
            print("\n1. Monthly Expenses Trend")
            print("2. Spending by Category")
            print("3. Spending Distribution")
            viz_choice = input("\nChoose visualization (1-3): ").strip()

            if viz_choice == '1':
                tracker.show_monthly_expenses()
            elif viz_choice == '2':
                tracker.show_spending_by_category()
            elif viz_choice == '3':
                tracker.show_spending_distribution()
            else:
                print("Invalid choice!")

        # Option 10: Save to CSV
        elif choice == '10':
            path = input("Enter filename to save (e.g., my_transactions.csv): ").strip()
            if not path:
                path = "transactions.csv"
            success, message = tracker.save_to_csv(path)
            print(message)

        # Option 11: Exit
        elif choice == '11':
            print("\nExiting the Personal Finance Tracker. Goodbye!")
            break

        else:
            print("\nInvalid option! Please choose between 0-11.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()