import streamlit as st
import pandas as pd
from utils import sales_rep
from openai import OpenAI

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")



client = OpenAI(api_key=api_key)

# Example DataFrame for performance data
# (Replace this with your actual performance_df dataframe)

# Example DataFrame for performance data
# (Replace this with your actual performance_df dataframe)
performance_df = pd.DataFrame({
    'Sales Representative': ['Alice', 'Bob', 'Charlie', 'John'],
    'Max Sales Category': ['Electronics', 'Clothing', 'Books', 'Home Appliances'],
    'Current Month Max Sales Volume': [10, 8, 12, 15],
    'Previous Month Max Sales Volume': [7, 10, 9, 18]
})

# Define the sales representatives
sales_representatives = performance_df['Sales Representative'].unique().tolist()

# Streamlit title
st.title("Sales Representative Performance Overview")

# Dropdown to select the sales representative
sales_rep_name = st.selectbox('Select a Sales Representative:', options=["Select"] + sales_representatives)

# Visualize the entire performance_df dataframe
st.subheader("Full Performance Data")
st.dataframe(performance_df)

# Check if a valid sales rep is selected (not the placeholder 'Select')
if sales_rep_name != "Select":
    st.markdown(f"### Selected Sales Representative: {sales_rep_name}")
    
    # Call the sales_rep function with performance_df and sales_rep_name
    output = sales_rep(performance_df, sales_rep_name)
    
    # Display the output from the sales_rep function
    st.markdown("### Motivational Feedback:")
    st.markdown(f"{output}")
    
    # Show the specific row of performance data for the selected sales representative
    st.subheader(f"Performance Data for {sales_rep_name}")
    sales_rep_data = performance_df[performance_df['Sales Representative'] == sales_rep_name]
    st.dataframe(sales_rep_data)
else:
    st.warning("Please select a sales representative from the dropdown above.")

