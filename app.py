import streamlit as st
import pandas as pd
from utils import sales_rep
from openai import OpenAI
import random
import pandas as pd
from datetime import datetime, timedelta
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


def generate_sales_data(num_records):
    sales_representatives = ['John', 'Alice', 'Bob', 'Charlie']
    product_categories = ['Electronics', 'Clothing', 'Home Appliances', 'Books']
    
    sales_data = []
    
    for _ in range(num_records):
        sales_rep = random.choice(sales_representatives)
        time = random.randint(0, 23)
        product_category = random.choice(product_categories)
        date = datetime.now() - timedelta(days=random.randint(0, 60))  # Limiting to recent 2 months
        
        sales_data.append({
            'Sales Representative': sales_rep,
            'Time': time,
            'Product Category': product_category,
            'Date': date
        })
    
    return pd.DataFrame(sales_data)

def get_max_sales_category(df):
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    
    # Calculate max sales category for each representative over all data
    max_sales_category = df.groupby('Sales Representative')['Product Category'].apply(lambda x: x.value_counts().idxmax())
    
    # Get current and previous month details
    current_month = datetime.now().month
    current_year = datetime.now().year
    last_month = (current_month - 1) if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    # Current month and previous month sales filtering
    current_month_sales = df[(df['Month'] == current_month) & (df['Year'] == current_year)]
    last_month_sales = df[(df['Month'] == last_month) & (df['Year'] == last_month_year)]
    
    # Max sales category dataframe
    max_sales_category_df = pd.DataFrame({
        'Sales Representative': max_sales_category.index, 
        'Max Sales Category': max_sales_category.values
    })
    
    # For each representative, count sales volume of their max sales category in the current month
    def get_sales_volume(df, category_df, month_df, month_name):
        volume_data = []
        for _, row in category_df.iterrows():
            rep = row['Sales Representative']
            max_category = row['Max Sales Category']
            
            # Filter the month sales for the representative's max category
            sales_volume = month_df[(month_df['Sales Representative'] == rep) & (month_df['Product Category'] == max_category)].shape[0]
            
            volume_data.append(sales_volume)
        
        category_df[f'{month_name} Max Sales Volume'] = volume_data
        return category_df

    # Calculate sales volumes for current month and previous month in the max category
    max_sales_category_df = get_sales_volume(df, max_sales_category_df, current_month_sales, "Current Month")
    max_sales_category_df = get_sales_volume(df, max_sales_category_df, last_month_sales, "Previous Month")
    
    return max_sales_category_df

# Generate sales data and get the best performance by category
sales_df = generate_sales_data(100)
performance_df = get_max_sales_category(sales_df)


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

