# Interactive Financial Dashboard

**A Dynamic Dashboard to Visualize Stock or ETF Performance and Metrics Over a Defined Period Using Python and Plotly**

## Overview
This project provides an interactive financial dashboard using Python and Plotly Dash to analyze and visualize the growth of selected stocks or ETFs over a user-defined period. The dashboard offers powerful features that help investors and analysts understand market movements and key financial metrics, with a particular focus on the SPY ETF, but it's customizable for other tickers as well.

## Features
- **Interactive Line Chart**: Visualize the daily percentage change of selected stocks or ETFs. Positive changes are displayed in green, while negative changes are shown in red.
- **Dynamic Bar Chart**: Provides a bar chart version of the daily percentage change, helping you quickly spot trends.
- **Annual Percentage Growth Calculation**: Automatically calculate and display the annual growth percentage for your chosen stock or ETF.
- **Rolling Correlation Analysis**: View the rolling correlation of your selected assets over time to understand their relationships.
- **Cumulative Returns and Performance Metrics**: Explore the cumulative returns of your investments over the specified period, visualizing the potential growth of an initial investment.

## How to Use
1. **Clone the Repository**: Clone this repository to your local machine to start using the dashboard.
   ```sh
   git clone https://github.com/InnovateWithAlex/interactive_financial_dashboard.git
   cd interactive_financial_dashboard
   ```
2. **Install Dependencies**: Install the necessary Python packages using the following command:
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Dashboard**: Use the following command to run the dashboard locally:
   ```sh
   python dashboard.py
   ```
4. **Open in Browser**: Once the server is running, open your web browser and go to `http://127.0.0.1:8050/` to interact with the dashboard.

## Project Structure
- **`dashboard.py`**: The main Python script to run the Plotly Dash dashboard.
- **`requirements.txt`**: A list of Python packages required for the project (e.g., `plotly`, `dash`, `yfinance`, `pandas`).
- **`data/`**: (Optional) A directory for any historical stock data that you may want to save for offline analysis.

## Technologies Used
- **Python**: Main programming language used.
- **Plotly Dash**: A web-based framework for building interactive visualizations.
- **Yahoo Finance (yfinance)**: API used to collect historical financial data.
- **Pandas**: Library used for data manipulation and analysis.

## Getting Started
To get started, make sure you have Python 3.7+ installed on your system. Clone the repository and install the required libraries using `pip`.

### Prerequisites
- Python 3.7+
- `pip` (Python package installer)

### Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/InnovateWithAlex/interactive_financial_dashboard.git
   ```
2. **Navigate to the Project Directory**:
   ```sh
   cd interactive_financial_dashboard
   ```
3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
- **Run the Dashboard**:
  ```sh
  python dashboard.py
  ```
- **Navigate to the Dashboard**: Once running, open your browser at `http://127.0.0.1:8050/` to view the dashboard.

## Customizing for Other Stocks or ETFs
The dashboard is designed to work with any stock or ETF symbol available through Yahoo Finance. Simply modify the stock symbols in `dashboard.py` to analyze the performance of different assets.

## Screenshots
![Dashboard Example 1](images/dashboard_screenshot_1.png)
![Dashboard Example 2](images/dashboard_screenshot_2.png)

## Contributing
Contributions are welcome! If you'd like to improve the functionality, fix a bug, or add new features, please:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- Yahoo Finance for providing historical data.
- Plotly for making financial data visualization simple and beautiful.
