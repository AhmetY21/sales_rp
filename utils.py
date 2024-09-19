import streamlit as st
from openai import OpenAI
import datetime
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")



client = OpenAI(api_key=api_key)

# Load environment variables from .env file





client = OpenAI(api_key=api_key)
def destination_city(date):
    # Convert the date string to a datetime object
    datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    
    # Define the mapping of months to capital cities
    capital_cities = {
        1: "Paris",
        2: "Berlin",
        3: "Rome",
        4: "Madrid",
        5: "London",
        6: "Athens",
        7: "Tokyo",
        8: "Beijing",
        9: "Moscow",
        10: "Washington, D.C.",
        11: "Ottawa",
        12: "Canberra"
    }
    
    # Get the month from the datetime object
    month = datetime_obj.month
    
    # Return the capital city based on the month
    return capital_cities.get(month, "Ankara")

def fortune_teller(date):
    #print(f"Your Destination city is {destination_city(date)} \n")
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a fortune teller and you give fancy responses based on the provided destination city . \
             Combine some short fortune based on the given destination city and  Use emojis while providing responses."},
            {"role": "user", "content": f"{destination_city(date)}"}
        ]
    )
    fortune_response = f"Your Destination city is {destination_city(date)} \n"+response.choices[0].message.content
    return fortune_response


def sales_rep(performance_df, sales_rep_name):
    # Filter the dataframe for the selected sales representative
    sales_rep_data = performance_df[performance_df['Sales Representative'] == sales_rep_name]
    
    if sales_rep_data.empty:
        return f"Sales representative '{sales_rep_name}' not found in the performance data."

    # Extract the relevant information for the sales representative
    max_sales_category = sales_rep_data['Max Sales Category'].values[0]
    current_max_sales_volume = sales_rep_data['Current Month Max Sales Volume'].values[0]
    previous_max_sales_volume = sales_rep_data['Previous Month Max Sales Volume'].values[0]
    
    # Set up the prompt for GPT-3.5-turbo
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "You are a store manager who makes motivational talks with sales representatives based on their performance. "
                           "You give motivational feedback by comparing the sales performance of this month and the previous month. "
                           "Encourage the sales rep to perform better. Use emojis for encouragement and positivity."
            },
            {
                "role": "user",
                "content": (
                    f"{sales_rep_name} has sold {current_max_sales_volume} units of {max_sales_category} this month, "
                    f"and {previous_max_sales_volume} units last month."
                )
            }
        ]
    )

    # Generate the final motivational message response
    motivational_response = response.choices[0].message.content
    
    return motivational_response

