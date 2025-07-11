#  Personal Finance Tracker

A Python-based CLI tool to manage, analyze, and visualize personal financial transactions. Built with pandas, matplotlib, and robust error handling.

## Features

### File Management
- Import transactions from `sampledata.csv` (validates format: date, category, description, amount)
- Export updated transactions to a new CSV file

###  Transaction Management
- Add, edit, delete, and view transactions (filterable by date)
- Data stored in a `pandas.DataFrame` with user input validation

###  Expense Analysis
- View spending by category
- Calculate monthly average spending
- Identify highest-spend category

###  Data Visualization
- **Line chart**: Monthly spending trends
- **Bar chart**: Total expenses per category
- **Pie chart**: Percentage distribution of spending

###  User-Friendly CLI
- Interactive text menu to navigate all features

##  Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
