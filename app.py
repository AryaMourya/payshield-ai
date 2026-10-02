"""Streamlit application entry point."""

import importlib


try:
	st = importlib.import_module("streamlit")
except ModuleNotFoundError as exc:
	raise RuntimeError(
		"Streamlit is required to run this app. Install it with: pip install streamlit"
	) from exc
import pandas as pd

st.set_page_config(
	layout="wide"
)
st.title("🛡️ PayShield AI")
st.subheader("Expense Analyzer and Digital Payment Safety Dashboard")

uploaded_file = st.file_uploader(
    "Upload your expense CSV file",
    type=["csv"]
)
if uploaded_file is not None:
	df = pd.read_csv(uploaded_file)
else:
	try:
		df = pd.read_csv("expense_transactions.csv")
		st.info("Using the sample expense dataset.")
	except FileNotFoundError:
		st.warning("Please upload an expense CSV file.")
		st.stop()

required_columns = {"date","amount","category"}

if not required_columns.issubset(df.columns):
	st.error(
		"CSV must contain these columns:date, amount, category"
    )
	st.stop()
	
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"],errors="coerce")

df= df.dropna(subset=["date","amount","category"])
df["month"] = df["date"].dt.to_period("M").astype(str)

total_spending = df["amount"].sum()
average_transaction = df["amount"].mean()
transaction_count = len(df)

category_totals = (
	df.groupby("category")["amount"]
	.sum()
	.sort_values(ascending=False)
)

top_category = category_totals.index[0]

#Dashboard metrics
col1,col2,col3,col4 = st.columns(4)

col1.metric(
	"Total Spending",
	f"₹{total_spending:,.2f}"
)

col2.metric(
    "Average Transaction",
    f"₹{average_transaction:,.2f}"
)

col3.metric(
    "Transactions",
    transaction_count
)

col4.metric(
    "Top Category",
    top_category
)
st.divider()

# Budget section
st.subheader("Monthly Budget")

months = df["month"].nunique()
suggested_budget = total_spending / max(months, 1)

st.write(
    f"Suggested monthly budget: ₹{suggested_budget:,.2f}"
)

budget = st.number_input(
    "Set your monthly budget",
    min_value=0.0,
    value=float(round(suggested_budget, 2)),
    step=500.0
)

latest_month = sorted(df["month"].unique())[-1]
latest_spending = df[df["month"] == latest_month]["amount"].sum()

months = df["month"].nunique()
suggested_budget = total_spending / max(months, 1)

st.write(
    f"Suggested monthly budget: ₹{suggested_budget:,.2f}"
)

budget = st.number_input(
    "Set your monthly budget",
    min_value=0.0,
    value=5000.0,
    step=500.0,
    key="monthly_budget"
)

latest_month = sorted(df["month"].unique())[-1]
latest_spending = df[df["month"] == latest_month]["amount"].sum()

if latest_spending > budget:
    st.error(
        f"Budget exceeded in {latest_month} by "
        f"₹{latest_spending - budget:,.2f}"
    )
else:
    st.success(
        f"Remaining budget for {latest_month}: "
        f"₹{budget - latest_spending:,.2f}"
    )

# Category chart
st.subheader("Spending by Category")
st.bar_chart(category_totals)

# Monthly chart
st.subheader("Monthly Spending")
monthly_totals = (
    df.groupby("month")["amount"]
    .sum()
    .sort_index()
)

st.line_chart(monthly_totals)

# Payment method chart
if "payment_method" in df.columns:
    st.subheader("Spending by Payment Method")

    payment_totals = (
        df.groupby("payment_method")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(payment_totals)

# Large transactions
st.subheader("Unusually Large Expenses")

# Large transactions
st.subheader("Unusually Large Expenses")

q1 = df["amount"].quantile(0.25)
q3 = df["amount"].quantile(0.75)
iqr = q3 - q1
limit = q3 + 1.5 * iqr

unusual_expenses = (
    df[df["amount"] > limit]
    .sort_values("amount", ascending=False)
)

if unusual_expenses.empty:
    st.success("No unusually large expenses detected.")
else:
    st.warning(
        f"{len(unusual_expenses)} unusually large "
        "expense(s) detected."
    )
    st.dataframe(
        unusual_expenses,
        use_container_width=True
    )

# Full transaction table
st.subheader("All Transactions")

st.dataframe(
    df.sort_values("date", ascending=False),
    use_container_width=True
)



# Download processed data
csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Processed CSV",
    data=csv_data,
    file_name="processed_expenses.csv",
    mime="text/csv"
)

