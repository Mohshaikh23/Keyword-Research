import requests
import json 
import streamlit as st
import pandas as pd
import os
import plotly.express as px

@st.cache_data
def keyword_research_by_url(url, location, api_key):
    url = "https://google-keyword-insight1.p.rapidapi.com/urlkeysuggest/"
    querystring = {"url": url, "location": location, "lang": "en"}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "google-keyword-insight1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # Save data to JSON and CSV
    with open('ex.json', 'w') as f:
        json.dump(data, f)
    df = pd.DataFrame(data)
    df.to_csv(f"data1/{url}_{location}.csv", index=False)
    return df

@st.cache_data
def keyword_research_by_keyword(keyword, location, api_key):
    filename = f"{keyword}.json"

    # Check if data already exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        st.write("Loaded data from cache.")
    else:
        url = "https://google-keyword-insight1.p.rapidapi.com/keysuggest/"
        querystring = {"keyword": keyword, "location": location, "lang": "en"}

        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "google-keyword-insight1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Save data to JSON
        with open(filename, 'w') as f:
            json.dump(data, f)
        st.write("Fetched new data from API.")

    df = pd.DataFrame(data)
    df.to_csv(f"data2/{keyword}_{location}.csv", index=False)
    return df

st.header("Keyword Research from Google Keyword Insight")
st.write("This project leverages an API - Google keyword Insight from Rapid API to gather keyword data and analyze various metrics such as search volume, competition level, and bid ranges. Our goal is to extract valuable insights that can help businesses optimize their online presence and drive targeted traffic.")

with st.sidebar:
    st.header("Search Section")
    api_key = st.text_input("API KEY")
    col1,col2 =st.columns(2)
    keyword = col1.text_input('keyword')
    location = col2.text_input('location')
    submit = st.button('Submit')

if submit:
    data = keyword_research_by_keyword(keyword,location,api_key)
    st.dataframe(data,use_container_width=True)

    # Creating visualizations with Plotly
    st.subheader("Keyword Analysis")
    
    # Volume distribution
    st.subheader("Volume distribution")
    st.markdown("""
                1. **Volume Distribution Histogram**: This histogram shows the distribution of search volumes for the keywords. It helps to visualize how many keywords fall within different volume ranges.""")
    fig_volume = px.histogram(data, x='volume', title='Volume Distribution', 
                               labels={'volume': 'Search Volume'}, nbins=20)
    st.plotly_chart(fig_volume)
    st.markdown("""
                **Interpretation**: 
                - This histogram displays the distribution of search volumes for the keywords. The x-axis represents the search volume, while the y-axis shows the count of keywords that fall into each volume range.

                **Insights**:
                - **High Search Volume**: If the histogram shows a significant number of keywords with high search volumes, it indicates potential opportunities for traffic. You might want to target those keywords in your SEO strategy.
                - **Low Search Volume**: A concentration of keywords with low search volumes suggests niche areas that may be worth exploring, especially if competition is also low.                
                """)
    

    # Competition Level Pie Chart
    st.subheader("Competition Level Pie Chart")
    st.markdown("""
                2. **Competition Level Pie Chart**: This pie chart displays the distribution of keywords across different competition levels (e.g., low, medium, high). It gives a quick overview of the proportion of keywords in each competition category.""")
    fig_competition = px.pie(data, names='competition_level', 
                              title='Competition Level Distribution', 
                              values='volume')
    st.plotly_chart(fig_competition)
    st.markdown("""
                **Interpretation**:
                - This pie chart visualizes the proportion of keywords categorized by competition levels (e.g., low, medium, high).

                **Insights**:
                - **Dominant Competition Levels**: If a large percentage of keywords fall under "low competition," this indicates an opportunity for easier ranking on search engines.
                - **Balanced Competition**: A mix of low, medium, and high competition can suggest a balanced strategy: targeting both low-competition keywords for quick wins and high-competition keywords for longer-term gains.               
                """)

    # Scatter Plot for Low vs High Bids
    st.subheader("Scatter Plot for Low vs High Bids")
    st.markdown("""
                3. **Scatter Plot for Low vs. High Bids**: This scatter plot allows you to see the relationship between the low and high bids for keywords. Different colors represent different competition levels, making it easier to identify trends in bid prices relative to competition.""")
    fig_bids = px.scatter(data, x='low_bid', y='high_bid', 
                          color='competition_level', 
                          title='Low Bid vs High Bid',
                          labels={'low_bid': 'Low Bid', 'high_bid': 'High Bid'},
                          hover_name='text')
    st.plotly_chart(fig_bids)
    st.markdown("""
                **Interpretation**:
                - This scatter plot shows the relationship between low and high bids for keywords, with colors representing different competition levels.

                **Insights**:
                - **Price Variation**: If you notice that high-competition keywords have higher bids, it indicates that advertisers are willing to invest more in these keywords, potentially due to their higher conversion rates.
                - **Market Trends**: Clusters of points in the scatter plot may reveal trends; for instance, if low bids correlate with high competition, it may suggest that many advertisers are targeting those keywords.               
                """)
    
    # Trend Analysis
    st.subheader("Trend Analysis")
    st.markdown("""
                4. **Trend Analysis Line Chart**: This line chart shows the trend of each keyword. It provides insights into how the trend score varies across different keywords.""")
    fig_trend = px.line(data, x='text', y='trend', 
                        title='Trend Analysis', 
                        labels={'text': 'Keyword', 'trend': 'Trend'})
    st.plotly_chart(fig_trend)
    st.markdown("""
                **Interpretation**:
                - This line chart displays the trend scores for each keyword, allowing you to see how interest in those keywords changes over time.

                **Insights**:
                - **Rising Trends**: Keywords with increasing trend scores suggest growing interest and may be worth targeting for timely content creation or marketing strategies.
                - **Declining Trends**: Keywords with decreasing trends might be losing relevance, indicating a need to pivot away from those terms.
                """)

    # Competition Index Box Plot
    st.subheader("Competition Index Box Plot")
    st.markdown("""
                5. **Competition Index Box Plot**: This box plot visualizes the competition index values, giving you insights into the spread and outliers in the competition levels for your keywords.""")
    fig_comp_index = px.box(data, y='competition_index', 
                             title='Competition Index Box Plot',
                             labels={'competition_index': 'Competition Index'})
    st.plotly_chart(fig_comp_index)
    st.markdown("""
                **Interpretation**:
                - This box plot visualizes the distribution of competition index values for keywords, highlighting medians, quartiles, and potential outliers.

                **Insights**:
                - **Overall Competition**: The spread of competition index values can inform you about the overall competitiveness of your target keywords. A tight interquartile range may suggest a consistent level of competition, while a wide range may indicate varied difficulty across keywords.
                - **Outliers**: Identifying outliers in the competition index can reveal exceptionally competitive keywords that might warrant special strategies or caution.
                """)
    
    st.subheader("General Insights")
    st.markdown("""
            - **Balanced Keyword Strategy**: Aim for a mix of keywords across competition levels to diversify traffic sources. Focus on low-competition keywords for quick wins while developing strategies for higher-competition keywords over time.
            - **Continuous Monitoring**: Regularly analyze trends and volume changes, as they can inform your content marketing strategy and SEO efforts. Being aware of shifts in keyword performance can help you stay ahead of competitors.
            - **Adaptation to Market Changes**: Use insights from bid and trend analyses to adapt your advertising strategies and content creation efforts. If certain keywords show promising trends, consider investing more in those areas.
                """)
    
    # Filter for high-volume, low-competition keywords
    st.subheader("High-Volume, Low-Competition Keywords")
    high_volume_low_comp = data[(data['volume'] > data['volume'].median()) & (data['competition_level'] == 'LOW')]

    # Display the filtered DataFrame
    st.dataframe(high_volume_low_comp, use_container_width=True)

    # High Volume vs. Low Competition Scatter Plot
    st.markdown("""
                **High-Volume, Low-Competition Keywords**: These are prime candidates for targeting in SEO strategies. They offer significant search volume with relatively low competition, making them easier to rank for.
                """)
    fig_vol_low_comp = px.scatter(high_volume_low_comp, x='volume', y='low_bid', 
                                title='High Volume vs. Low Competition Keywords (Low Bid)', 
                                labels={'volume': 'Search Volume', 'low_bid': 'Low Bid'},
                                hover_name='text')
    st.plotly_chart(fig_vol_low_comp)

    # Filter for keywords with high bids
    st.subheader("Keywords with High Bids")
    high_bids = data[(data['low_bid'] > data['low_bid'].median()) & (data['high_bid'] > data['high_bid'].median())]

    # Display the filtered DataFrame
    st.dataframe(high_bids, use_container_width=True)

    # Scatter Plot for High Bids
    st.markdown("""
                **High Bids Keywords**: Keywords with high bids are valuable because advertisers are willing to pay more for these terms, signaling their importance and likely conversion potential.
                """)
    fig_high_bids = px.scatter(high_bids, x='low_bid', y='high_bid', 
                            color='competition_level', 
                            title='Keywords with High Bids',
                            labels={'low_bid': 'Low Bid', 'high_bid': 'High Bid'},
                            hover_name='text')
    st.plotly_chart(fig_high_bids)

    # Filter for trending keywords
    st.subheader("Trending Keywords")
    trending_keywords = data[data['trend'] > data['trend'].median()]

    # Display the filtered DataFrame
    st.dataframe(trending_keywords, use_container_width=True)

    # Line chart for trending keywords
    st.markdown("""
                **Trending Keywords**: These keywords have growing interest, and capitalizing on them early can yield higher visibility in search engines or advertising campaigns.
                """)
    fig_trending = px.line(trending_keywords, x='text', y='trend', 
                        title='Trending Keywords',
                        labels={'text': 'Keyword', 'trend': 'Trend'})
    st.plotly_chart(fig_trending)

    # High Volume, High Bid, and Trending Combo Analysis
    st.subheader("High Volume, High Bid, Trending Keywords")
    high_value_keywords = data[(data['volume'] > data['volume'].median()) & 
                            (data['low_bid'] > data['low_bid'].median()) & 
                            (data['trend'] > data['trend'].median())]

    # Display the filtered DataFrame
    st.dataframe(high_value_keywords, use_container_width=True)

    # Scatter Plot for High-Value Keywords (Volume, Low Bid, Trend)
    st.markdown("""
                **High-Value Keywords**: These keywords combine high search volume, significant bid prices, and trending interest. They are the most valuable for both SEO and paid campaigns.
                """)
    fig_high_value = px.scatter(high_value_keywords, x='volume', y='trend', 
                                color='low_bid', 
                                title='High Volume, High Bid, Trending Keywords',
                                labels={'volume': 'Search Volume', 'trend': 'Trend'},
                                hover_name='text')
    st.plotly_chart(fig_high_value)
