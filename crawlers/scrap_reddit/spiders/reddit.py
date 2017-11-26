# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from crawlers.scrap_reddit.items import ScrapRedditItem
import os
import logging

class RedditSpider(CrawlSpider):

    start_urls = []

    def set_subreddits(self):
        for sub in self.subreddits.split(';'):
            self.start_urls.append("https://www.reddit.com/r/" + sub)

    name = "reddit"
    allowed_domains = ["reddit.com"]

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
                restrict_xpaths=('//span[@class="next-button"]',)
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        self.set_subreddits()
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        items = []

        logging.log(logging.INFO, "URL: " + response.url)
        page = response.text
        soup = BeautifulSoup(page, "lxml")

        lista = soup.find("div", {"id": "siteTable"})

        dados_reddit = {}
        lista_dados = []

        for l in lista:

            score = l.find("div", {"class": "score likes"})

            if score is not None:

                subreddit = l["data-subreddit"]

                if l.find("a", {"class": "bylink comments may-blank"}) is None:
                    continue

                comments_link = l.find("a", {"class": "bylink comments may-blank"})['data-href-url']
                thread_link = l.find("a", {"class": "bylink comments may-blank"})['href']

                l.find("a", {"class": "title may-blank"})
                title = l.a.text

                if title == '' and l.find("a", "title may-blank ") is not None:
                    title = l.find("a", "title may-blank ").text

                if title == '' and l.find("a", "title may-blank outbound") is not None:
                    title = l.find("a", "title may-blank outbound").text

                if score.text == '•':
                    upvote = 0
                else:
                    upvote = int(score['title'])

                if upvote < 5000:
                    continue

                dados_reddit["subreddit"] = subreddit
                dados_reddit["comments_link"] = comments_link
                dados_reddit["thread_link"] = thread_link
                dados_reddit["title"] = title
                dados_reddit["upvote"] = upvote

                lista_dados.append(dados_reddit)

                item = ScrapRedditItem()

                item['subreddit'] = dados_reddit["subreddit"]
                item['comments_link'] = dados_reddit["comments_link"]
                item['thread_link'] = dados_reddit["thread_link"]
                item['title'] = dados_reddit["title"]
                item['upvote'] = dados_reddit["upvote"]

                logging.log(logging.INFO, "Item: " + str(item))

                items.append(item)

        return items

if __name__ == "__main__":

    subreddits = "cats"

    if os.path.exists("result.json"):
        os.remove("result.json")

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json'
    })

    process.crawl(RedditSpider, subreddits=subreddits)
    process.start()

