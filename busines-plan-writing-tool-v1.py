import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io

# Main app structure
st.set_page_config(page_title="Business Startup Tool", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
pages = ["Dashboard", "Business Plan", "Financial Projections", "Market Analysis", "Export"]
selection = st.sidebar.radio("Go to", pages)

# Initialize session state for storing data
if 'business_data' not in st.session_state:
    st.session_state.business_data = {
        'name': '',
        'description': '',
        'mission': '',
        'vision': '',
        'financials': pd.DataFrame(),
        'market_data': pd.DataFrame()
    }

# Dashboard Page
def dashboard():
    st.title("Startup Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Business Overview")
        if st.session_state.business_data['name']:
            st.write(f"Name: {st.session_state.business_data['name']}")
            st.write(f"Description: {st.session_state.business_data['description']}")
        else:
            st.write("No business information entered yet")
    
    with col2:
        st.subheader("Quick Stats")
        if not st.session_state.business_data['financials'].empty:
            revenue = st.session_state.business_data['financials']['Revenue'].sum()
            expenses = st.session_state.business_data['financials']['Expenses'].sum()
            st.metric("Total Projected Revenue", f"${revenue:,.2f}")
            st.metric("Total Projected Expenses", f"${expenses:,.2f}")
            st.metric("Net Profit", f"${revenue - expenses:,.2f}")

# Business Plan Page
def business_plan():
    st.title("Business Plan")
    
    st.session_state.business_data['name'] = st.text_input("Business Name")
    st.session_state.business_data['description'] = st.text_area("Business Description")
    st.session_state.business_data['mission'] = st.text_area("Mission Statement")
    st.session_state.business_data['vision'] = st.text_area("Vision Statement")
    
    if st.button("Save Business Plan"):
        st.success("Business plan saved successfully!")

# Financial Projections Page
def financial_projections():
    st.title("Financial Projections")
    
    # Input form for financial data
    st.subheader("Add Monthly Projection")
    with st.form(key='financial_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            month = st.selectbox("Month", range(1, 13))
            year = st.number_input("Year", min_value=2025, value=2025)
        with col2:
            revenue = st.number_input("Projected Revenue", min_value=0.0)
        with col3:
            expenses = st.number_input("Projected Expenses", min_value=0.0)
        submit = st.form_submit_button("Add Projection")
        
        if submit:
            new_data = pd.DataFrame({
                'Month': [f"{year}-{month:02d}"],
                'Revenue': [revenue],
                'Expenses': [expenses]
            })
            if st.session_state.business_data['financials'].empty:
                st.session_state.business_data['financials'] = new_data
            else:
                st.session_state.business_data['financials'] = pd.concat(
                    [st.session_state.business_data['financials'], new_data]
                )
            st.success("Projection added!")
    
    # Display financial chart
    if not st.session_state.business_data['financials'].empty:
        df = st.session_state.business_data['financials']
        fig = px.line(df, x='Month', y=['Revenue', 'Expenses'], 
                     title='Financial Projections')
        st.plotly_chart(fig)
        st.dataframe(df)

# Market Analysis Page
def market_analysis():
    st.title("Market Analysis")
    
    st.subheader("Market Size and Growth")
    market_size = st.number_input("Estimated Market Size ($)", min_value=0.0)
    growth_rate = st.number_input("Expected Growth Rate (%)", min_value=0.0)
    
    st.subheader("Competitor Analysis")
    competitor = st.text_input("Competitor Name")
    strength = st.text_area("Competitor Strengths")
    weakness = st.text_area("Competitor Weaknesses")
    
    if st.button("Add Competitor"):
        new_data = pd.DataFrame({
            'Competitor': [competitor],
            'Strengths': [strength],
            'Weaknesses': [weakness]
        })
        if st.session_state.business_data['market_data'].empty:
            st.session_state.business_data['market_data'] = new_data
        else:
            st.session_state.business_data['market_data'] = pd.concat(
                [st.session_state.business_data['market_data'], new_data]
            )
        st.success("Competitor added!")
    
    if not st.session_state.business_data['market_data'].empty:
        st.dataframe(st.session_state.business_data['market_data'])

# Export Page
def export():
    st.title("Export Business Plan")
    
    # Create export content
    buffer = io.StringIO()
    buffer.write(f"# Business Plan\n\n")
    buffer.write(f"## Company Overview\n")
    buffer.write(f"Name: {st.session_state.business_data['name']}\n")
    buffer.write(f"Description: {st.session_state.business_data['description']}\n")
    buffer.write(f"Mission: {st.session_state.business_data['mission']}\n")
    buffer.write(f"Vision: {st.session_state.business_data['vision']}\n")
    
    if not st.session_state.business_data['financials'].empty:
        buffer.write("\n## Financial Projections\n")
        buffer.write(st.session_state.business_data['financials'].to_string())
    
    if not st.session_state.business_data['market_data'].empty:
        buffer.write("\n## Market Analysis\n")
        buffer.write(st.session_state.business_data['market_data'].to_string())
    
    # Download button
    st.download_button(
        label="Download Business Plan",
        data=buffer.getvalue(),
        file_name=f"{st.session_state.business_data['name']}_business_plan.txt",
        mime="text/plain"
    )

# Page routing
page_dict = {
    "Dashboard": dashboard,
    "Business Plan": business_plan,
    "Financial Projections": financial_projections,
    "Market Analysis": market_analysis,
    "Export": export
}

if selection in page_dict:
    page_dict[selection]()
