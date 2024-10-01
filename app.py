import streamlit as st
import requests
import pandas as pd
import json
import os
import matplotlib.pyplot as plt


# Function to get keyword data from Ubersuggest API
def get_keyword_data(keyword, country):
    url = "https://ubersuggest-keyword-ideas.p.rapidapi.com/keyword-Overview-Data"
    
    querystring = {"keyword": keyword, "country": country}
    
    headers = {
        "x-rapidapi-key": "aa47eb9625msh2084a2c9f3c7716p19a4dcjsnac584c6c0af7",
        "x-rapidapi-host": "ubersuggest-keyword-ideas.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    # Return the JSON response if status code is 200
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to process keyword data and extract necessary info
def process_keyword_data(data):
    # First check if the data is a list and not empty
    if isinstance(data, list) and len(data) > 0:
        keyword_overview = data[0].get("Keyword Overview", [])
        google_trends_data = data[0].get("Google Trends Data", {}).get("Interest Google Trends Data", [])
        
        # Check if keyword overview is not empty
        if keyword_overview:
            overview_data = keyword_overview[0]  # Process the first keyword overview
            search_volume = overview_data.get("Search Volume", 0)
            keyword_difficulty = overview_data.get("Keyword Difficulty", 0)
            high_cpc = overview_data.get("High CPC", "N/A")
            low_cpc = overview_data.get("Low CPC", "N/A")
            trend_data = overview_data.get("Trend", [])

            # Convert the trend data to a DataFrame for easier manipulation
            df_trend = pd.DataFrame(trend_data)
            
            # Create a summary DataFrame for keyword overview
            df_keyword = pd.DataFrame({
                "Search Volume": [search_volume],
                "Keyword Difficulty": [keyword_difficulty],
                "High CPC": [high_cpc],
                "Low CPC": [low_cpc]
            })
            
            return df_keyword, df_trend
        else:
            st.write("No keyword overview data available.")
            return pd.DataFrame(), pd.DataFrame()  # Empty DataFrames in case of missing data
    else:
        st.write("Data structure is not a list or it's empty.")
        return pd.DataFrame(), pd.DataFrame()  # Empty DataFrames in case of failure


def save_json_to_file(data, keyword):
    directory = "data"
    # Ensure the directory exists, if not create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Create the full file path
    file_path = os.path.join(directory, f"{keyword}_data.json")
    
    # Save the JSON data to file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Data saved to {file_path}")
    
    # Provide a download button in Streamlit
    st.download_button(
        label="Download JSON",
        data=json.dumps(data, indent=4),
        file_name= f"{data}.json",
        mime="application/json"
    )


# Function to process Google Trends data
def process_google_trends_data(data):
    if data:
        # Extract Google Trends data
        google_trends_data = data[1].get("Google Trends Data", {}).get("Interest Google Trends Data", [])
        df_trends = pd.DataFrame(google_trends_data)
        return df_trends
    return None

# Function to plot keyword difficulty and search volume as bar chart
def plot_keyword_difficulty_and_volume(df_keyword, keyword):
    if 'Keyword Difficulty' in df_keyword.columns and 'Search Volume' in df_keyword.columns:
        fig, ax = plt.subplots(figsize=(8, 4))
        df_keyword[['Keyword Difficulty', 'Search Volume']].plot(kind='bar', ax=ax, color=['#FF6347', '#4682B4'])
        plt.title(f'Keyword Difficulty & Search Volume for: {keyword}')
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        st.pyplot(fig)

# Function to plot search trend over months as line chart
def plot_search_trends(df_trends, keyword):
    if 'month' in df_trends.columns and 'searches' in df_trends.columns:
        st.line_chart(df_trends.set_index('month')['searches'], width=0, height=0)
        st.subheader(f'Search Trends Over Time for: {keyword}')
        
# Function to plot interest in regions as bar chart
def plot_google_trends_region(df_trends, keyword):
    if 'region' in df_trends.columns and 'interest' in df_trends.columns:
        fig, ax = plt.subplots(figsize=(8, 4))
        df_trends.plot(kind='bar', x='region', y='interest', ax=ax, color='#8A2BE2')
        plt.title(f'Regional Interest for: {keyword}')
        plt.xlabel('Region')
        plt.ylabel('Interest')
        plt.xticks(rotation=90)
        st.pyplot(fig)

# Displaying the keyword data and charts
def display_keyword_data_and_charts(data, keyword):
    # Get the two DataFrames from process_keyword_data
    df_keyword, df_trends = process_keyword_data(data)

    if df_keyword is not None:
        st.subheader(f"Keyword Overview for: {keyword}")
        st.dataframe(df_keyword)
        
        # Plot Keyword Difficulty and Search Volume
        plot_keyword_difficulty_and_volume(df_keyword, keyword)
    
    if not df_trends.empty:
        st.subheader(f"Google Trends Data for: {keyword}")
        st.dataframe(df_trends)
        
        # Plot Search Trends Over Time
        plot_search_trends(df_trends, keyword)
        
        # Plot Regional Interest from Google Trends
        plot_google_trends_region(df_trends, keyword)

        # st.line_chart(df_trends.set_index("month")["searches"])



# Streamlit App Structure
def main():
    st.title("Keyword Research Tool using Ubersuggest API")

    # Input for multiple keywords
    keywords = st.text_area("Enter keywords (comma-separated):", value="Python, SEO, Data Science")
    
    # Input for country code
    country = st.text_input("Enter country code (e.g., 'in' for India, 'us' for USA):", value="in")
    
    # Button to trigger the API call
    if st.button("Get Keyword Data"):
        # Split keywords into a list
        keyword_list = [keyword.strip() for keyword in keywords.split(",")]
        
        # Iterate over each keyword
        for keyword in keyword_list:
            st.write(f"Fetching data for: **{keyword}**")
            
            # Fetch data for the keyword
            data = get_keyword_data(keyword, country)
            
            if data:
                save_json_to_file(data, keyword)

                # Display data and charts
                display_keyword_data_and_charts(data, keyword)

                # Process and display keyword overview data
                df_keyword = process_keyword_data(data)

                if df_keyword is not None:
                    st.subheader(f"Keyword Overview for: {keyword}")
                    st.dataframe(df_keyword)
                else:
                    st.write(f"No keyword overview data available for: {keyword}")
                
                # Process and display Google Trends data
                df_trends = process_google_trends_data(data)
                if df_trends is not None:
                    st.subheader(f"Google Trends Data for: {keyword}")
                    st.dataframe(df_trends)
                else:
                    st.write(f"No Google Trends data available for: {keyword}")
            else:
                st.write(f"Failed to fetch data for: {keyword}")

# Run the Streamlit app
if __name__ == '__main__':
    main()
