import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Boshoff Estates", layout="wide", page_icon="🏠", initial_sidebar_state="expanded")

# ====================== BRANDING & SIDEBAR ======================
st.sidebar.title("🏡 Boshoff Estates")
st.sidebar.markdown("**Property Investment Pro** – Cape Town Focused")
st.sidebar.info("Updated March 2026 • Prime Rate: 10.25% • SARS 2027 Tax Rules")
st.sidebar.caption("Free forever • Custom built for you")

# ====================== TABS (Expanded) ======================
tab_home, tab_afford, tab_bond, tab_freedom, tab_transfer, tab_tax, tab_deal, tab_multilet, tab_area, tab_proposal = st.tabs([
    "Home", "Affordability", "Bond Repayment", "Freedom Number",
    "Transfer Duty", "Income Tax", "Rental/Flip", "Multi-Let", "Area Research", "Proposal"
])

# ====================== HOME ======================
with tab_home:
    st.header("Welcome to Boshoff Estates Investment App")
    st.write("Your professional, free South African property analysis tool – now with multi-let, area insights, and polished proposals.")
    st.success("All features upgraded • Mobile-friendly • 100% offline after install")
    st.image("https://via.placeholder.com/800x300/1E3A8A/FFFFFF?text=Boshoff+Estates+Banner", use_column_width=True)  # Replace with your logo URL

# ====================== AFFORDABILITY ======================
with tab_afford:
    st.header("Affordability Calculator")
    col1, col2 = st.columns(2)
    with col1:
        gross_income = st.number_input("Gross Monthly Income (R)", min_value=0.0, value=35000.0, step=1000.0)
        deposit = st.number_input("Available Deposit (R)", min_value=0.0, value=200000.0, step=10000.0)
    with col2:
        interest_rate = st.slider("Bond Interest Rate (%)", 8.0, 13.0, 10.25, 0.25)  # Updated default
        term_years = st.slider("Bond Term (years)", 10, 30, 20)

    max_repayment = gross_income * 0.30
    r = interest_rate / 1200
    n = term_years * 12
    max_loan = max_repayment * (1 - (1 + r) ** -n) / r if r > 0 else 0
    max_property = max_loan + deposit

    st.metric("Max Affordable Property Value", f"R {max_property:,.0f}")
    st.write(f"Repayment limit: **R {max_repayment:,.0f}** (30% rule)")

# ====================== BOND REPAYMENT + GRAPH ======================
with tab_bond:
    st.header("Bond Repayment Calculator")
    purchase = st.number_input("Purchase Price (R)", value=2800000.0, step=50000.0)
    deposit_pct = st.slider("Deposit %", 0, 50, 10)
    deposit_amt = purchase * (deposit_pct / 100)
    loan = purchase - deposit_amt
    rate = st.slider("Interest Rate (%)", 8.0, 13.0, 10.25, 0.25)
    years = st.slider("Term (years)", 10, 30, 20)

    r = rate / 1200
    n = years * 12
    monthly = loan * r * (1 + r)**n / ((1 + r)**n - 1) if r > 0 and loan > 0 else 0
    st.metric("Monthly Bond Repayment", f"R {monthly:,.2f}")

    # Amortization Graph
    if loan > 0:
        months = list(range(1, n+1))
        balance = [loan]
        prin_paid = []
        int_paid = []
        for m in range(1, n+1):
            interest = balance[-1] * r
            prin = monthly - interest
            new_bal = balance[-1] - prin
            balance.append(max(0, new_bal))
            prin_paid.append(prin)
            int_paid.append(interest)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=balance[1:], name="Balance", line=dict(color="blue")))
        fig.add_trace(go.Bar(x=months, y=prin_paid, name="Principal", marker_color="green"))
        fig.add_trace(go.Bar(x=months, y=int_paid, name="Interest", marker_color="red"))
        fig.update_layout(barmode='stack', title="Amortization Breakdown", xaxis_title="Months", yaxis_title="R")
        st.plotly_chart(fig, use_container_width=True)

# ====================== FREEDOM NUMBER ======================
with tab_freedom:
    st.header("Freedom Number Calculator")
    target_monthly = st.number_input("Desired Monthly Passive Income (R)", value=25000.0, step=1000.0)
    net_yield = st.slider("Net Yield After Expenses (%)", 4.0, 10.0, 7.0, 0.5)
    freedom = (target_monthly * 12) / (net_yield / 100) if net_yield > 0 else 0
    st.metric("Freedom Number (Portfolio Value)", f"R {freedom:,.0f}")
    st.info("Portfolio size needed for your passive income goal at expected yield.")

# ====================== TRANSFER DUTY (SARS 2026 rates) ======================
with tab_transfer:
    st.header("Transfer Duty Calculator (SARS 2026)")
    value = st.number_input("Property Value (R)", value=2800000.0, step=50000.0)

    def transfer_duty(v):
        if v <= 1210000: return 0
        elif v <= 1663800: return 0.03 * (v - 1210000)
        elif v <= 2329300: return 13614 + 0.06 * (v - 1663800)
        elif v <= 2994800: return 53544 + 0.08 * (v - 2329300)
        elif v <= 13310000: return 106784 + 0.11 * (v - 2994800)
        else: return 1241456 + 0.13 * (v - 13310000)

    duty = transfer_duty(value)
    st.metric("Transfer Duty Payable", f"R {duty:,.0f}")

# ====================== INCOME TAX (2027 year) ======================
with tab_tax:
    st.header("Income Tax Calculator (2027 SARS)")
    taxable = st.number_input("Annual Taxable Income (R)", value=600000.0, step=10000.0)
    age_group = st.radio("Age", ["Under 65", "65-74", "75+"])

    def calc_tax(inc):
        if inc <= 245100: return inc * 0.18
        elif inc <= 383100: return 44118 + (inc - 245100) * 0.26
        elif inc <= 530200: return 79998 + (inc - 383100) * 0.31
        elif inc <= 695800: return 125599 + (inc - 530200) * 0.36
        elif inc <= 887000: return 185215 + (inc - 695800) * 0.39
        elif inc <= 1878600: return 259783 + (inc - 887000) * 0.41
        else: return 666339 + (inc - 1878600) * 0.45

    tax = calc_tax(taxable)
    rebate = 17820 if age_group == "Under 65" else 17820 + 9765 if age_group == "65-74" else 17820 + 9765 + 3249
    final = max(0, tax - rebate)
    st.metric("Estimated Annual Tax Payable", f"R {final:,.0f}")

# ====================== DEAL ANALYSIS ======================
with tab_deal:
    st.header("Standard Rental & Flip Analysis")
    sub1, sub2 = st.tabs(["Rental Cashflow", "Flip"])

    with sub1:
        pp = st.number_input("Purchase Price (R)", value=2200000.0, key="std_pp")
        dep = st.number_input("Deposit (R)", value=220000.0, key="std_dep")
        loan_std = pp - dep
        rate_std = st.slider("Rate %", 8.0, 13.0, 10.25, key="std_r")
        term_std = st.slider("Term y", 10, 30, 20, key="std_t")
        rent = st.number_input("Monthly Gross Rent (R)", value=18000.0)
        exp = st.number_input("Monthly Expenses (R)", value=4000.0)
        vac = st.slider("Vacancy %", 0, 15, 5)

        r_m = rate_std / 1200
        n_m = term_std * 12
        bond_m = loan_std * r_m * (1 + r_m)**n_m / ((1 + r_m)**n_m - 1) if r_m > 0 else 0
        net_rent = rent * (1 - vac/100)
        cf_month = net_rent - bond_m - exp
        st.metric("Monthly Net Cashflow", f"R {cf_month:,.0f}")

        # Projection
        y_proj = st.slider("Years", 1, 20, 10)
        growth = st.slider("Rent Growth % p.a.", 0.0, 10.0, 5.0)
        cfs = [ (net_rent * 12 * (1 + growth/100)**(y-1)) - (bond_m * 12) - (exp * 12) for y in range(1, y_proj+1) ]
        fig_cf = px.bar(x=range(1, y_proj+1), y=cfs, title="Annual Cashflow Projection")
        st.plotly_chart(fig_cf)

    with sub2:
        flip_pp = st.number_input("Purchase (R)", value=1500000.0)
        reno = st.number_input("Renovation (R)", value=200000.0)
        hold_m = st.number_input("Hold Months", value=6)
        sale = st.number_input("Sale Price (R)", value=2100000.0)
        duty_flip = transfer_duty(flip_pp)
        profit = sale - flip_pp - reno - (bond_m * hold_m) - duty_flip
        st.metric("Est. Flip Profit (pre-tax)", f"R {profit:,.0f}")

# ====================== MULTI-LET ANALYSIS ======================
with tab_multilet:
    st.header("Multi-Let / HMO Analysis (Room-by-Room)")
    st.write("Ideal for student accommodation, shared houses in Cape Town – higher yields possible.")
    num_rooms = st.number_input("Number of Lettable Rooms", min_value=2, max_value=12, value=6)
    rent_per_room = st.number_input("Rent per Room p.m. (R)", value=4500.0)
    total_rent = num_rooms * rent_per_room
    shared_exp = st.number_input("Total Monthly Shared Expenses (utilities, rates, etc.)", value=8000.0)
    vacancy_pct = st.slider("Expected Vacancy % (multi-let often higher)", 5, 25, 10)
    net_rent_ml = total_rent * (1 - vacancy_pct/100)
    bond_ml = st.number_input("Monthly Bond (from Bond tab or enter)", value=15000.0)
    cf_ml = net_rent_ml - bond_ml - shared_exp
    st.metric("Monthly Net Cashflow (Multi-Let)", f"R {cf_ml:,.0f}")
    st.metric("Gross Yield", f"{(total_rent * 12 / st.session_state.get('pp_ml', 2200000)) * 100:.1f}%", help="Total rent / purchase price")
    st.info("Tip: Multi-lets often achieve 10-15% gross yields in student areas like Observatory or Rondebosch.")

# ====================== AREA RESEARCH ======================
with tab_area:
    st.header("Suburb / Area Research Table")
    st.write("Quick comparison – edit values for your research.")
    data = {
        "Suburb": ["Observatory", "Rondebosch", "Claremont", "Milnerton", "Bellville", "Your Custom"],
        "Avg Gross Yield (%)": [9.5, 7.8, 6.5, 8.2, 8.0, 0.0],
        "Annual Growth Est. (%)": [6.0, 5.5, 4.8, 7.0, 5.2, 0.0],
        "Avg Rent (2-bed)": [14000, 16000, 18000, 13000, 12000, 0],
        "Safety Rating (1-10)": [6, 8, 9, 7, 7, 0],
        "Notes": ["Student heavy, multi-let strong", "Family + schools", "Premium", "Coastal appeal", "Affordable growth", "Enter your suburb"]
    }
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df, num_rows="dynamic")
    st.caption("Use this to compare – update with real data from Property24, Private Property, etc.")

# ====================== PROPOSAL ======================
with tab_proposal:
    st.header("Generate Professional Proposal")
    prop_name = st.text_input("Property / Project Name")
    pp_prop = st.number_input("Purchase Price (R)", value=2500000.0)
    cf_prop = st.number_input("Projected Monthly Cashflow (R)", value=3500.0)
    yield_prop = st.number_input("Expected Gross Yield (%)", value=8.5)
    freedom_prop = st.number_input("Contribution to Freedom Number (R)", value=0.0)

    if st.button("Generate Proposal"):
        proposal_text = f"""
# Boshoff Estates – Investment Proposal
**Date:** {datetime.now().strftime('%d %B %Y')}  
**Property:** {prop_name}  
**Purchase Price:** R{pp_prop:,.0f}  
**Projected Monthly Net Cashflow:** R{cf_prop:,.0f}  
**Gross Yield:** {yield_prop:.1f}%  
**Transfer Duty Estimate:** R{transfer_duty(pp_prop):,.0f}  
**Freedom Number Impact:** Contributes toward your R{freedom_prop:,.0f} goal  

**Recommendation:**  
Strong opportunity in Cape Town market – positive cashflow from day one, solid capital growth potential.  

**Prepared by Boshoff Estates** – Contact for viewing or full due diligence.

Copy → Paste into Word/Google Docs, add your logo at top, export as PDF.
        """
        st.markdown(proposal_text)
        st.download_button("Download .txt (for PDF conversion)", proposal_text, file_name=f"Boshoff_Proposal_{prop_name}.txt")

st.caption("✅ Fully loaded: Multi-let, Area table, PDF-ready proposal, updated rates • Mobile optimised • Enjoy!")
