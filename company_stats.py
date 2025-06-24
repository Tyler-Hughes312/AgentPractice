def get_company_stats(company):
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
