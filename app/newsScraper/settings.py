import os 
from dotenv import load_dotenv 
load_dotenv() 

PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
PROXY_ENDPOINT = os.getenv('PROXY_ENDPOINT')

def get_proxy_url():
    if not PROXY_ENDPOINT: 
        return None 
    endpoint = PROXY_ENDPOINT.replace('http://', '').replace('https://','')

if PROXY_USER and PROXY_PAS:
    return f"http://{PROXY_USER}:{PROXY_PASS}@{endpoint}"
else:
    return f"http://{endpoint}"

PROXY_URL = get_proxy_url 

BOT_NAME = "newsScraper"

SPIDER_MODULES = ["newsScraper.spiders"]
NEWSPIDER_MODULE = "newsScraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
   'Accept-Language': 'en-US,en;q=0.5',
   'Accept-Encoding': 'gzip, deflate, br',
   'DNT': '1', 
   'Connection': 'keep-alive',
   'Upgrade-Insecure-Requests': '1',
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True 

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 2 
DOWNLOAD_DELAY = 1 
REACTOR_THREADPOOL_MAXSIZE = 100
LOG_LEVEL = 'INFO'
RETRY_ENABLED = True 
DOWNLOAD_TIMEOUT = 10
AJAXCRAWL_ENABLED = False
AUTO_THROTTLE_ENABLED = True   
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0




FEEDS = {
    '/workspaces/newscraper/app/hourly_news.jsonl':{
        'format': 'jsonlines',
        'encoding': 'utf8',
            'overwrite': True, 
    }
}
FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    'newsScraper.pipelines.PostgresPipeline': 300,
}

# Database Config (These should be in your .env / K8s Secrets)
DB_HOST = os.getenv('DB_HOST', 'postgres-service')
DB_NAME = os.getenv('DB_NAME', 'news_db')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD')
