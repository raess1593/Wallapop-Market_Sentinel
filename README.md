# 🛒 Wallapop Market Sentinel 🛡️

An automated Data Engineering pipeline designed to scrape, process, and analyze real-time market data from Wallapop. This tool allows users to track price trends, identify market opportunities, and perform statistical analysis on any product category with a single command. In addition, it is included a real-world analysis searching for Nike products.

## 📊 Market Insights at a Glance
<a href="analysis.ipynb">
  <img src="output/price_density.png" alt="Market Analysis" width="550">
</a>
<a href="analysis.ipynb">
  <img src="output/outstanding_vs_standard.png" alt="Market Analysis" width="475">
</a>

*Click the images to explore the full interactive analysis in the Jupyter Notebook.*

## 🌟 Key Features
* **Dynamic Scraping:** Fully customizable search keywords and item limits via CLI arguments.
* **Shadow DOM Interaction:** Advanced Selenium implementation to handle modern web components and dynamic loading.
* **Automated Data Refinery:** Cleans raw currency strings and translates product titles from Spanish to English for international analysis.
* **Headless Execution:** Runs in the background (invisible mode) to ensure a smooth user experience.
* **Statistical Laboratory:** Integrated Jupyter Notebook for high-end data visualization and outlier detection using the Interquartile Range (IQR).

## 📁 Project Structure
* **`main.py`**: The entry point. Handles user parameters and orchestrates the pipeline.
* **`scraper.py`**: The engine. Manages browser automation and raw data extraction. It closes automatically once finished.
* **`processor.py`**: The refinery. Transforms "dirty" web strings into clean, numeric data ready for math.
* **`analysis.ipynb`**: The visual lab. Loads the generated CSV to produce professional market insights.
* **`data/`**: Directory where all extracted CSV files are stored.

## 🚀 Getting Started

### Prerequisites
* Python 3

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/Wallapop-Market-Sentinel.git](https://github.com/your-username/Wallapop-Market-Sentinel.git)
   cd Wallapop-Market-Sentinel

2. Install necessary dependencies:
    ```bash
    pip install -r requirements.txt

## Usage

Run the scraper by specifying your desired keyword and the number of items:

  ```bash
    # Example: Search for 200 Nike items
    python main.py --search "nike" --limit 200
  ```

**Note:** The scraper runs in headless mode. Simply wait for the process to finish and check the `data/` folder for your `.csv` file.

## 📈 Data Analysis

Once you have your **CSV**, open `analysis.ipynb` to visualize the market. The notebook includes:

- **Price Distribution (Boxplot):** Identifies the "normal" price range and highlights statistical outliers.
- **Market Density (Histogram):** Shows where the majority of sellers are pricing their products.
- **Promotion Impact (Bar Chart):** Analyzes if "**Outstanding**" items are priced higher than standard listings.

> **Tip:** You can reuse the same notebook for any search term by updating the file path to your latest CSV.

## 🛠️ Built With

- **Python** (Automation & Logic)
- **Selenium** (Web Scraping)
- **Pandas** & **NumPy** (Data Processing)
- **Seaborn** & **Matplotlib** (Visualization)
