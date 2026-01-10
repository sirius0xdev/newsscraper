📊 NewsScraper & LLM Pipeline
A distributed news extraction system designed to crawl articles from 200+ sources, store them in a PostgreSQL database, and provide a clean dataset for the Gemma LLM to process on an hourly schedule.

🏗 Architecture Overview
The system operates in a "Producer-Consumer" model within a Kubernetes cluster:

The Producer (Scrapy): A CronJob that reads URLs from a ConfigMap, scrapes clean article text, and inserts it into Postgres.

The Storage (Postgres): Acts as the source of truth, handling deduplication via URL hashing.

The Consumer (Gemma): A secondary CronJob that triggers after the scraper finishes, querying the latest news for analysis.

🚀 Getting Started
1. Prerequisites
Docker & Kubernetes Cluster

PostgreSQL (Running inside the cluster as postgres-service)

Python 3.12+ (for local development)

2. Environment Variables (.env)
Create a .env file in the root directory to handle secrets:

Bash

# Proxy Configuration
PROXY_ENDPOINT=your.proxy.com:8080
PROXY_USER=username  # Leave blank for public proxies
PROXY_PASS=password  # Leave blank for public proxies

# Database Configuration
DB_HOST=postgres-service
DB_NAME=news_db
DB_USER=admin
DB_PASSWORD=yoursecurepassword
3. Installation
Bash

pip install -r requirements.txt
🛠 Project Structure
Plaintext

.
├── newsScraper/           # Scrapy project folder
│   ├── spiders/           # NewsSpider logic
│   ├── pipelines.py       # Postgres integration
│   ├── middlewares.py     # Proxy and User-Agent rotation
│   └── settings.py        # Scrapy & AutoThrottle config
├── Dockerfile             # Multi-stage production build
├── .dockerignore          # Security & build optimization
├── requirements.txt       # Project dependencies
└── k8s/                   # Kubernetes manifests (CronJobs, Secrets, ConfigMaps)
📦 Deployment
Build the Image
Bash

docker build -t your-registry/news-scraper:latest .
docker push your-registry/news-scraper:latest
Kubernetes Setup
URLs: Update the news-urls ConfigMap with your urls.txt.

Secrets: Apply your proxy-credentials and db-credentials.

CronJobs: Apply the manifests in the /k8s folder.

📈 Data Estimates
Sites: 200

Articles: ~1,000 / hour

Storage Growth: ~240 MB / day

Retention: Suggested cleanup of articles older than 48 hours to keep the DB size under 1GB.

⚖️ License
This project is for educational/research purposes. Ensure compliance with the robots.txt and Terms of Service of target news organizations.
