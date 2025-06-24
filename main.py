import autogen
import os
import pandas as pd
from dotenv import load_dotenv
import requests

os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(dotenv_path=".env", override=True)

def google_search(query: str, api_key: str, cx: str, num_results: int = 20, company: str = ""):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cx,
        "num": min(num_results, 10)  # Google API max per request is 10
    }
    headlines = []
    links = []
    start = 1
    while len(headlines) < num_results:
        params["start"] = start
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        items = results.get("items", [])
        for item in items:
            link = item.get("link", "")
            title = item.get("title", "")
            # Exclude company website and non-news domains
            if company.lower() not in link.lower() and "news" in link.lower():
                headlines.append(title)
                links.append(link)
            elif company.lower() not in link.lower() and any(domain in link.lower() for domain in ["cnn", "nytimes", "bbc", "reuters", "forbes", "bloomberg", "wsj", "cnbc", "guardian", "apnews", "npr", "foxnews", "abcnews", "usatoday", "latimes", "nbcnews", "newsweek", "time", "businessinsider", "marketwatch", "yahoo", "msnbc", "politico", "axios", "fortune", "barrons", "investopedia", "cbsnews", "washingtonpost", "theverge", "techcrunch", "wired", "engadget", "theatlantic", "slate", "huffpost", "vice", "buzzfeed", "vox", "aljazeera", "dw.com", "cbc.ca", "globalnews.ca", "ctvnews.ca", "sky.com", "independent.co.uk", "telegraph.co.uk", "ft.com", "economist.com", "scmp.com", "straitstimes.com", "japantimes.co.jp", "smh.com.au", "afr.com", "theage.com.au", "sbs.com.au", "abc.net.au"]):
                headlines.append(title)
                links.append(link)
        if len(items) < params["num"]:
            break  # No more results
        start += params["num"]
    return headlines[:num_results], links[:num_results]

def get_autogen_assistant():
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    config_list = [
        {
            "model": "claude-3-opus-20240229",
            "api_key": anthropic_api_key,
            "api_type": "anthropic"
        }
    ]
    anthropic_llm_config = {
        "config_list": config_list,
        "temperature": 0.3,
    }
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=anthropic_llm_config,
        system_message="You are a helpful assistant that can answer questions and help with tasks."
    )
    return assistant

def rate_headlines_with_llm(df, assistant):
    ratings = []
    for headline in df["headline"]:
        prompt = (
            "You are an investor interested in innovation and stock prices. "
            "Rate the following news headline for the company on a scale of 1-10: "
            "1-4 = objectively bad for the company (1 is worst), 5-6 = neutral, 7-10 = good for the company (10 is best). "
            "Only return the number.\nHeadline: " + headline
        )
        response = assistant.generate_reply([{"role": "user", "content": prompt}])
        print(f"Prompt: {prompt}\nResponse: {response}")  # Debug print
        try:
            rating = int(''.join(filter(str.isdigit, str(response))))
        except Exception:
            rating = None
        ratings.append(rating)
    df["popularity_rating"] = ratings
    return df

def get_company_stats(company):
    # Use Yahoo Finance API (yfinance) for market cap, revenue, etc.
    import yfinance as yf
    ticker = yf.Ticker(company)
    info = ticker.info
    stats = {
        "market_cap": info.get("marketCap", "N/A"),
        "revenue": info.get("totalRevenue", "N/A"),
        "employees": info.get("fullTimeEmployees", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "country": info.get("country", "N/A"),
    }
    return stats

def get_domain_popularity(link):
    # Ordered by general popularity (most to least)
    domain_order = [
        "cnn", "nytimes", "bbc", "reuters", "forbes", "bloomberg", "wsj", "cnbc", "guardian", "apnews", "npr", "foxnews", "abcnews", "usatoday", "latimes", "nbcnews", "newsweek", "time", "businessinsider", "marketwatch", "yahoo", "msnbc", "politico", "axios", "fortune", "barrons", "investopedia", "cbsnews", "washingtonpost", "theverge", "techcrunch", "wired", "engadget", "theatlantic", "slate", "huffpost", "vice", "buzzfeed", "vox", "aljazeera", "dw.com", "cbc.ca", "globalnews.ca", "ctvnews.ca", "sky.com", "independent.co.uk", "telegraph.co.uk", "ft.com", "economist.com", "scmp.com", "straitstimes.com", "japantimes.co.jp", "smh.com.au", "afr.com", "theage.com.au", "sbs.com.au", "abc.net.au"
    ]
    for i, domain in enumerate(domain_order):
        if domain in link.lower():
            return i
    return len(domain_order)  # Least popular if not found

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    company = input("Enter the company name or ticker symbol (for stats): ")
    query = input("Enter a Google search query: ")
    headlines, links = google_search("news " + query, api_key, cx, num_results=20, company=company)
    df = pd.DataFrame({"headline": headlines, "link": links})
    # Sort by domain popularity
    df["domain_popularity"] = df["link"].apply(get_domain_popularity)
    df = df.sort_values("domain_popularity").reset_index(drop=True)
    assistant = get_autogen_assistant()
    df = rate_headlines_with_llm(df, assistant)
    print(df)
    if not df.empty and df["popularity_rating"].notnull().any():
        avg_score = df["popularity_rating"].dropna().mean()
        print(f"\nAverage Popularity Score: {avg_score:.2f}")
    else:
        print("\nNo valid popularity ratings to average.")
    try:
        stats = get_company_stats(company)
        print("\nCompany Stats:")
        for k, v in stats.items():
            print(f"{k.replace('_', ' ').title()}: {v}")
    except Exception as e:
        print("Could not fetch company stats:", e)

if __name__ == "__main__":
    main()
