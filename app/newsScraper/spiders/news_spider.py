from w3lib.html import remove_tags_with_content, remove_tags
from pathlib import Path 
import scrapy
import re 
from urllib.parse import urlparse
import datetime 
class NewsSpider(scrapy.Spider):
    name = "articles"

    async def start(self):
        file_path = getattr(self, 'filename', 'urls.txt')
        if not Path(file_path).exists():
                self.logger.error(f"FILE NOT FOUND: {file_path}")
                return

        with open(file_path, "r") as f:
                for line in f:
                    urls = re.findall(r'https?://[^\s"]+', line)
                    for url in urls:
                        self.logger.info(f" Found and requesting: {url}")
                        yield scrapy.Request(url=url, callback=self.parse) 

    def parse(self, response):
        
        output_dir = Path("downloaded_pages")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        cleaned_html = remove_tags_with_content(
            response.text,
            which_ones=('script', 'style', 'nav', 'footer', 'header', 'aside' )
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
                                ''' ).get()


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
