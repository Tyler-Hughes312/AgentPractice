import requests

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
            elif company.lower() not in link.lower() and any(domain in link.lower() for domain in [
                "cnn", "nytimes", "bbc", "reuters", "forbes", "bloomberg", "wsj", "cnbc", "guardian", "apnews", "npr", "foxnews", "abcnews", "usatoday", "latimes", "nbcnews", "newsweek", "time", "businessinsider", "marketwatch", "yahoo", "msnbc", "politico", "axios", "fortune", "barrons", "investopedia", "cbsnews", "washingtonpost", "theverge", "techcrunch", "wired", "engadget", "theatlantic", "slate", "huffpost", "vice", "buzzfeed", "vox", "aljazeera", "dw.com", "cbc.ca", "globalnews.ca", "ctvnews.ca", "sky.com", "independent.co.uk", "telegraph.co.uk", "ft.com", "economist.com", "scmp.com", "straitstimes.com", "japantimes.co.jp", "smh.com.au", "afr.com", "theage.com.au", "sbs.com.au", "abc.net.au"]):
                headlines.append(title)
                links.append(link)
        if len(items) < params["num"]:
            break  # No more results
        start += params["num"]
    return headlines[:num_results], links[:num_results]

def get_domain_popularity(link):
    domain_order = [
        "cnn", "nytimes", "bbc", "reuters", "forbes", "bloomberg", "wsj", "cnbc", "guardian", "apnews", "npr", "foxnews", "abcnews", "usatoday", "latimes", "nbcnews", "newsweek", "time", "businessinsider", "marketwatch", "yahoo", "msnbc", "politico", "axios", "fortune", "barrons", "investopedia", "cbsnews", "washingtonpost", "theverge", "techcrunch", "wired", "engadget", "theatlantic", "slate", "huffpost", "vice", "buzzfeed", "vox", "aljazeera", "dw.com", "cbc.ca", "globalnews.ca", "ctvnews.ca", "sky.com", "independent.co.uk", "telegraph.co.uk", "ft.com", "economist.com", "scmp.com", "straitstimes.com", "japantimes.co.jp", "smh.com.au", "afr.com", "theage.com.au", "sbs.com.au", "abc.net.au"
    ]
    for i, domain in enumerate(domain_order):
        if domain in link.lower():
            return i
    return len(domain_order)  # Least popular if not found
