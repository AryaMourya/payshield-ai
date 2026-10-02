import streamlit as st
import pandas as pd
from html import escape

st.set_page_config(page_title="PayShield AI - Senior Mode", page_icon="🛡️", layout="wide")

# -------------------- Styling --------------------
def apply_senior_style(enabled):
    size = "24px" if enabled else "16px"
    heading = "36px" if enabled else "28px"
    button = "26px" if enabled else "16px"
    spacing = "1.4" if enabled else "1.2"
    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: {size}; line-height: {spacing}; }}
    h1 {{ font-size: {heading} !important; }}
    h2, h3 {{ font-size: {('30px' if enabled else '22px')} !important; }}
    .stButton > button, .stDownloadButton > button {{
        min-height: 58px; font-size: {button} !important;
        font-weight: 700; border-radius: 12px;
    }}
    .stMetric {{ padding: 12px; border-radius: 12px; border: 2px solid #dddddd; }}
    [data-testid="stDataFrame"] {{ font-size: {size}; }}
    </style>
    """, unsafe_allow_html=True)

# -------------------- State --------------------
if "senior_mode" not in st.session_state:
    st.session_state.senior_mode = True
if "payments_paused" not in st.session_state:
    st.session_state.payments_paused = False

with st.sidebar:
    st.header("Settings")
    senior_mode = st.toggle(
        "Senior Citizen Mode",
        value=st.session_state.senior_mode,
        help="Uses larger text, clearer buttons, and simpler explanations."
    )
    st.session_state.senior_mode = senior_mode
    apply_senior_style(senior_mode)

    st.divider()
    st.write("Language")
    language = st.selectbox("Choose language", ["English", "Hindi"], label_visibility="collapsed")

# -------------------- Header --------------------
st.title("🛡️ PayShield AI")
st.subheader("Simple and safer digital-payment assistance")

if senior_mode:
    st.info("Welcome. You can check your spending, find unusual payments, or pause payments in an emergency.")
else:
    st.caption("Prototype using synthetic transaction data. No real payments are connected.")

# -------------------- Load data --------------------
uploaded_file = st.file_uploader("Upload expense CSV", type=["csv"])

try:
    df = pd.read_csv(uploaded_file) if uploaded_file else pd.read_csv("expense_transactions.csv")
except FileNotFoundError:
    st.error("Please place expense_transactions.csv in the same folder as app.py.")
    st.stop()

required = {"date", "amount", "category"}
if not required.issubset(df.columns):
    st.error("CSV must contain: date, amount, and category columns.")
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna(subset=["date", "amount", "category"]).copy()
df["month"] = df["date"].dt.to_period("M").astype(str)

# -------------------- Emergency controls --------------------
st.header("Emergency Safety")
if st.session_state.payments_paused:
    st.error("Payments are PAUSED in this demo.")
    if st.button("Resume payments", use_container_width=True):
        st.session_state.payments_paused = False
        st.rerun()
else:
    st.warning("If you think someone is trying to scam you, pause payments before taking action.")
    if st.button("🚨 Pause payments", type="primary", use_container_width=True):
        st.session_state.payments_paused = True
        st.rerun()

st.divider()

# -------------------- Key metrics --------------------
total = df["amount"].sum()
average = df["amount"].mean()
category_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
latest_month = sorted(df["month"].unique())[-1]
latest_total = df.loc[df["month"] == latest_month, "amount"].sum()

st.header("Your Money at a Glance")
a, b, c = st.columns(3)
a.metric("Total spending", f"₹{total:,.0f}")
b.metric("Average payment", f"₹{average:,.0f}")
c.metric("Top category", str(category_totals.index[0]))

# -------------------- Spending explanation --------------------
st.header("Where did my money go?")
st.bar_chart(category_totals)

if senior_mode:
    top = category_totals.index[0]
    top_amount = category_totals.iloc[0]
    st.info(f"You spent the most on {top}: ₹{top_amount:,.0f}.")

# -------------------- Budget --------------------
st.header("Monthly Budget")
months = max(df["month"].nunique(), 1)
suggested = total / months
budget = st.number_input("Set monthly budget (₹)", min_value=0.0, value=float(round(suggested)), step=500.0)

if latest_total > budget:
    st.error(f"You spent ₹{latest_total:,.0f} in {latest_month}. This is ₹{latest_total-budget:,.0f} above your budget.")
else:
    st.success(f"You have ₹{budget-latest_total:,.0f} left for {latest_month}.")

# -------------------- Unusual transactions --------------------
st.header("Check for Unusual Payments")
q1 = df["amount"].quantile(.25)
q3 = df["amount"].quantile(.75)
limit = q3 + 1.5 * (q3 - q1)
unusual = df[df["amount"] > limit].sort_values("amount", ascending=False)

if unusual.empty:
    st.success("No unusually large payments were found.")
else:
    st.warning(f"Found {len(unusual)} payment(s) larger than ₹{limit:,.0f}.")
    st.dataframe(unusual, use_container_width=True, hide_index=True)
    st.write("If you do not recognize a payment, contact your bank using its official phone number. Do not share your PIN or OTP.")

# -------------------- Simple help --------------------
st.header("Need Help?")
help_text = {
    "English": "Never share your UPI PIN or OTP. A QR code is normally used to make a payment, not to receive money.",
    "Hindi": "अपना UPI PIN या OTP कभी साझा न करें। QR कोड आमतौर पर भुगतान करने के लिए होता है, पैसे प्राप्त करने के लिए नहीं।"
}
st.info(help_text[language])

if st.button("Show all transactions", use_container_width=True):
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("Download expense report", csv_bytes, "senior_mode_expense_report.csv", "text/csv", use_container_width=True)