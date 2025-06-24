import os
import pandas as pd
from dotenv import load_dotenv
from news_scraper import google_search, get_domain_popularity
from llm_rating import get_autogen_assistant, rate_headlines_with_llm
from company_stats import get_company_stats

os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(dotenv_path=".env", override=True)

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
