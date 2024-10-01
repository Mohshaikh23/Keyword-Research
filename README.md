# Google Keyword Research Tool

This project is a **Keyword Research Tool** built using **Streamlit** and **Google Keyword Insight API**. It allows users to perform keyword research by analyzing key metrics such as **search volume**, **competition level**, **low/high bids**, and **trend** to help improve SEO strategies, drive traffic, and optimize online marketing campaigns.


## Features

- **Keyword Research by Keyword**: Fetch relevant keyword suggestions for any given keyword.
- **Data Analysis & Visualization**: Gain insights with dynamic charts like volume distribution, competition level, bid ranges, and trends.
- **Downloadable Data**: Export data in CSV format for further analysis.
  
## Technologies Used

- **Python**: Backend logic and API integration.
- **Streamlit**: Frontend interface for an interactive web app.
- **Pandas**: Data manipulation and analysis.
- **Plotly**: Data visualization for interactive charts.
- **Google Keyword Insight API**: Fetch keyword data from Google.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Mohshaikh23/Keyword-Research.git
    ```
2. **Navigate and Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Get API Key**:
   - Sign up for a free account on [RapidAPI](https://rapidapi.com/) and subscribe to the [Google Keyword Insight API](https://rapidapi.com/google-keyword-insight1).

2. **Run the Streamlit App**:
   ```bash
   streamlit run main.py
   ```

3. **Input your API Key** and choose whether to search by URL or keyword:
   - Enter the **API key**, **keyword/URL**, and **location** in the sidebar.
   - Click the `Submit` button to fetch and display keyword data.

4. **Analyze the Data**:
   - View **data tables** and **interactive charts** for deeper keyword insights.
   - Identify **high-value keywords** with high search volumes, low competition, and trending potential.
  
## Metrics & Visualizations

- **Volume Distribution Histogram**: Understand the distribution of keyword search volumes.
- **Competition Level Pie Chart**: See the proportion of low, medium, and high-competition keywords.
- **Bid Price Scatter Plot**: Analyze the relationship between low and high bid prices for each keyword.
- **Trend Analysis Line Chart**: View keyword trends over time to identify rising or falling interest.

## File Structure

```bash
google-keyword-research-tool/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # List of Python dependencies
├── README.md             # Project documentation
└── data/                 # Folder to store fetched data (CSV/JSON)
```

## Example Output

The app displays the following metrics and charts:

1. **Volume Distribution**: A histogram showing the search volume distribution across keywords.
2. **Competition Levels**: A pie chart showing the distribution of keywords by competition level (low, medium, high).
3. **Low vs. High Bids**: A scatter plot to analyze low and high bids across different keywords.
4. **Trend Analysis**: A line chart to track the trend scores of keywords over time.

## API Usage

We use the **Google Keyword Insight API** to retrieve keyword suggestions and related metrics. This requires an API key from RapidAPI.

- **Endpoint for Keyword-based search**: `/keysuggest/`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with improvements or bug fixes.

## Contact

For any questions or feedback, please contact mohsin.shaikh324@gmail.com.
```

### Key Points Included:
- Project description
- Installation instructions
- Usage guide with API key setup
- Key features and metrics explained
- File structure outline
- Example outputs and API integration details
