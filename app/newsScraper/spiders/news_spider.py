from w3lib.html import remove_tags_with_content, remove_tags
from pathlib import Path
import scrapy
import re
from urllib.parse import urlparse, urljoin
import datetime
import feedparser


def is_rss_url(url):
    """Detect if a URL is likely an RSS/Atom feed."""
    url_lower = url.lower()
    rss_patterns = [
        '.rss', '.xml', '/feed/', '/feed/', '/rss/', 'rss.xml', '.rdf',
        '/arc/outboundfeeds/rss/', 'feedburner', 'outboundfeeds',
    ]
    for p in rss_patterns:
        if p in url_lower:
            return True
    # Also check if 'rss' or 'feed' appears as a path segment
    path = urlparse(url).path
    segments = [s for s in path.split('/') if s]
    for seg in segments:
        if seg.lower() in ('rss', 'feed', 'atom'):
            return True
    return False


class NewsSpider(scrapy.Spider):
    name = "articles"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()

    def start_requests(self):
        file_path = getattr(self, 'filename', 'urls.txt')
        if not Path(file_path).exists():
            self.logger.error(f"FILE NOT FOUND: {file_path}")
            return

        with open(file_path, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                urls = re.findall(r'https?://[^\s",]+', line)
                for url in urls:
                    # Strip trailing whitespace and comments
                    url = url.strip()
                    if url in self.seen_urls:
                        self.logger.debug(f"Skipping duplicate: {url}")
                        continue
                    self.seen_urls.add(url)

                    if is_rss_url(url):
                        self.logger.info(f"  RSS feed detected, will parse: {url}")
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse_rss_feed,
                            errback=self.errback,
                        )
                    else:
                        self.logger.info(f"  Found and requesting: {url}")
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse,
                            errback=self.errback,
                        )

    def errback(self, failure):
        """Handle request failures gracefully."""
        self.logger.error(
            f"Request failed: {failure.request.url} — {failure.value}"
        )

    def parse_rss_feed(self, response):
        """Parse RSS/Atom feed XML and yield requests for each article link."""
        try:
            feed = feedparser.parse(response.text)
        except Exception as e:
            self.logger.error(f"Failed to parse RSS feed {response.url}: {e}")
            return

        entries = feed.entries
        if not entries:
            # Try parsing raw XML as fallback
            feed = feedparser.parse(response.body)
            entries = feed.entries

        for entry in entries:
            link = getattr(entry, 'link', None)
            if not link:
                continue
            # Normalize: remove fragments
            link = link.split('#')[0].rstrip('/')
            if link in self.seen_urls:
                continue
            self.seen_urls.add(link)
            self.logger.info(f"  RSS article: {link}")
            yield scrapy.Request(
                url=link,
                callback=self.parse,
                errback=self.errback,
            )

        self.logger.info(
            f"Parsed {len(entries)} articles from feed: {response.url}"
        )

    def parse(self, response):

        output_dir = Path("downloaded_pages")
        output_dir.mkdir(parents=True, exist_ok=True)

        cleaned_html = remove_tags_with_content(
            response.text,
            which_ones=('script', 'style', 'nav', 'footer', 'header', 'aside')
        )

        sel = scrapy.Selector(text=cleaned_html)
        title = sel.xpath('//title/text()').get() or "No Title"
        article_html = sel.xpath('''//article |
                                 //main |

                                 //div[contains(@class, "post-content")] |
                                //div[contains(@class, "entry-content")] |
                                //div[contains(@class, "article-body")] |
                                //div[contains(@id, "story-body")] |
                                //body
                                ''').get()


        pure_text = remove_tags(article_html)




        final_url = response.url
        domain = urlparse(final_url).netloc.replace('www.', '')
        yield {
            'title': title,
            'url': final_url,
            'text': pure_text.strip(),
            'domain': domain,
            'timestamp': datetime.datetime.now().isoformat()
        }

        # path_parts = [p for p in urlparse(final_url).path.split('/') if p]

        #filename = "-".join(path_parts) if path_parts else "index"
        #full_path = output_dir / f"{filename[:50]}.html"
        #file_save_path = output_dir / filename
        #full_path.write_bytes(response.body)
        #self.logger.info(f"✅ Saved {filename}")
