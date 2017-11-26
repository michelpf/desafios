# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapRedditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    subreddit = scrapy.Field()
    comments_link = scrapy.Field()
    thread_link = scrapy.Field()
    title = scrapy.Field()
    upvote = scrapy.Field()

    pass
