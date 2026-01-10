# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
import os

class PostgresPipeline:
    def open_spider(self, spider):
        # Connect using environment variables
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        self.cur = self.connection.cursor()
        
        # Create table if it doesn't exist
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title TEXT,
                url TEXT UNIQUE,
                content TEXT,
                domain TEXT,
                timestamp TIMESTAMPTZ
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            self.cur.execute("""
                INSERT INTO articles (title, url, content, domain, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            """, (
                item['title'],
                item['url'],
                item['text'],
                item['domain'],
                item['timestamp']
            ))
            self.connection.commit()
        except Exception as e:
            spider.logger.error(f"Error saving to Postgres: {e}")
            self.connection.rollback()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

from itemadapter import ItemAdapter


class NewsscraperPipeline:
    def process_item(self, item, spider):
        return item


