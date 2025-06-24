# News Sentiment & Popularity Analyzer for Investors

This project scrapes the latest news headlines about a company, rates them for popularity and sentiment using an LLM (Anthropic Claude), and fetches key company statistics from Yahoo Finance. It is designed for investors interested in innovation and stock prices.

## Features
- Scrapes top news headlines using Google Custom Search API
- Filters for reputable news sources and excludes the company's own website
- Sorts headlines by news source popularity
- Uses an LLM to rate each headline (1-10 scale: 1-4 bad, 5-6 neutral, 7-10 good)
- Prints the average popularity/sentiment score
- Fetches company stats (market cap, revenue, employees, etc.) using Yahoo Finance

## Requirements
- Python 3.8+
- [Anthropic API key](https://console.anthropic.com/)
- [Google Custom Search API key and CX](https://programmablesearchengine.google.com/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)

Install dependencies:
```sh
pip install pandas requests python-dotenv yfinance anthropic autogen
```

## Setup
1. **.env file** (in project root):
   ```
   ANTHROPIC_API_KEY=your-anthropic-api-key
   GOOGLE_API_KEY=your-google-api-key
   GOOGLE_CX=your-google-cx
   ```
2. Make sure your Google Custom Search Engine is set to search the entire web.

## Usage
Run the script:
```sh
python main.py
```
- Enter the company name or ticker symbol (for stats)
- Enter a search query (e.g., the company name)

The script will:
- Print a DataFrame of news headlines, links, and LLM-generated popularity ratings
- Print the average popularity score
- Print company statistics

## Notes
- The LLM is prompted as an investor interested in innovation and stock prices.
- Ratings: 1-4 = bad, 5-6 = neutral, 7-10 = good for the company.
- Make sure your API keys are valid and not rate-limited.

