from scrapy.settings import Settings
import scrapydo
import sys, getopt
from crawlers.scrap_reddit.spiders.reddit import RedditSpider


def main(argv):
    scrapydo.setup()

    settings = Settings()
    settings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
    settings.set("FEED_FORMAT", "json")
    settings.set("FEED_URI", "result.json")

    try:
        opts, args = getopt.getopt(argv,"hs:",["subreddit="])
    except getopt.GetoptError:
        print('cli_crawler.py -s <lista de subreddit separado por vírgula, ex. programming;dogs;brazil>')
        sys.exit(2)

    if len(opts) == 0:
        print('cli_crawler.py -s <lista de subreddit separado por vírgula, ex. programming;dogs;brazil>')

    for opt, arg in opts:
        if opt == '-s':
            subreddits = arg
            print("Iniciando crawler para buscar dados dos subreddits " + subreddits + "...")
            data = scrapydo.run_spider(RedditSpider(), settings=settings, subreddits='askreddit')
            for item in data:

                if item["title"] == '':
                    title = "_No Title_ :("
                else:
                    title = item["title"]

                message = item["subreddit"] + ", votes " + str(item["upvote"]) + " " + "[" + title + "](" + \
                           item["thread_link"] + ") \n"

                print(message)

    sys.exit()


if __name__ == "__main__":
   main(sys.argv[1:])