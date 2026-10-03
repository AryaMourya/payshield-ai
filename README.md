# payshield-ai
An explainable digital payment safety and expense-analysis dashboard with Senior Citizen Mode, budget tracking, and unusual payment detection.

PayShield AI is an explainable digital payment safety and expense-analysis dashboard built in Python and Streamlit.
The project helps users understand their spending, monitor budgets, identify unusually large transactions, and access simple digital-payment safety guidance. It also includes a Senior Citizen Mode with larger text and simple explanations, bilingual safety guidance, and an emergency 
payment-pause control for demonstration purposes.

> This is a hackathon prototype. It uses synthetic transaction data and does not connect to real bank accounts, UPI accounts, or payment systems.

### Problem

Digital-payment users may find it difficult to:

- Understand where their money is being spent.
- Identify unusually large or suspicious transactions.
- Control monthly expenses.
- Recognize common payment scams.
- Use financial applications comfortably, especially senior citizens.

### Solution

PayShield AI provides a simple safety and financial-awareness layer that analyzes transaction data and presents understandable insights before users make financial decisions.

## Features

- Expense analysis by category.
- Monthly spending summaries.
- Custom monthly budget tracking.
- Detection of unusually large expenses using the IQR method.
- Payment-method analysis.
- CSV upload and processed-report download.
- Senior Citizen Mode.
- Large text and high-visibility controls.
- English and Hindi safety guidance.
- Simulated emergency payment-pause control.
- Explainable results instead of unexplained risk scores.

## Technology Stack

- Python
- Pandas
- Streamlit
- Matplotlib
- Seaborn
- CSV-based synthetic dataset

## Project Structure

```text
payshield-ai/
├── app.py
├── expense_transactions.csv
├── requirements.txt
└── README.md
```
