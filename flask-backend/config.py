# config.py
import os

# config.py
ALLOWED_DOMAINS = {
    "google", "youtube", "amazon", "facebook", "twitter", "instagram", "wikipedia", "linkedin", 
    "pinterest", "tumblr", "reddit", "github", "stackoverflow", "quora", "medium", "wordpress",
    "chrome", "apple", "microsoft", "yahoo", "netflix", "adobe", "paypal", "reddit", "github", "dropbox",
    "salesforce", "bbc", "cnn", "espn", "nytimes", "forbes", "huffpost", "washingtonpost", "ebay",
    "walmart", "target", "homedepot", "bestbuy", "costco", "bankofamerica", "chase", "wellsfargo",
    "usbank", "citi", "capitalone", "spotify", "pinterest", "whatsapp", "tiktok", "snapchat", "slack",
    "zoom", "shopify", "cloudflare", "mozilla", "oracle", "intel", "ibm", "nvidia", "tesla", "uber",
    "lyft", "airbnb", "booking", "tripadvisor", "expedia", "hotels", "kayak", "skyscanner", "delta",
    "southwest", "united", "americanexpress", "visa", "mastercard", "discover", "stripe", "square",
    "intuit", "quickbooks", "mailchimp", "godaddy", "bluehost", "hostgator", "wordpress", "medium",
    "quora", "stackexchange", "stackoverflow", "bitbucket", "sourceforge", "heroku", "bitly", "reuters",
    "aljazeera", "weather", "bloomberg", "seekingalpha", "investopedia", "cdc", "nih", "who", "mayoclinic",
    "webmd", "medlineplus", "healthline", "nasa", "whitehouse", "gov", "europa", "parliament", 
    "nationalgeographic", "unicef", "unesco", "redcross", "worldbank", "imf", "humanesociety", 
    "change", "craigslist", "indeed", "monster", "glassdoor", "simplyhired", "ziprecruiter", "taleo",
    "adp", "groupon", "live", "outlook", "icloud", "protonmail", "yandex", "vk", "baidu", "qq", "taobao",
    "tmall", "jd", "weibo", "sina", "alibaba", "1688", "flipkart", "rakuten", "mercadolibre", "jumia",
    "souq", "konga", "olx", "carrefour", "zara", "hm", "nike", "adidas", "puma", "underarmour", 
    "ralphlauren", "gap", "oldnavy", "sephora", "ulta", "maccosmetics", "lorealparis", "dior", "chanel",
    "gucci", "prada", "hermes", "versace", "burberry", "vogue", "elle", "gq", "vanityfair", 
    "scientificamerican", "popsci", "techcrunch", "wired", "arstechnica", "engadget", "theverge", 
    "cnet", "gsmarena", "9to5mac", "macrumors", "xda-developers", "hackaday", "barrons", "economist",
    "wsj", "ft", "yelp", "trip", "aaa", "flyertalk", "hilton", "marriott", "ihg", "hyatt", "spg", 
    "choicehotels", "radisson", "wyndham", "holidayinn", "fourseasons", "ritzcarlton", "sonesta", 
    "telegram", "whatsapp"
}

MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/phishing")
MODEL_TYPE = os.getenv("MODEL_TYPE", "DNN")
