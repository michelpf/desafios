from pip._vendor.requests.packages.urllib3.util import timeout
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
from crawlers.scrap_reddit.spiders.reddit import RedditSpider
import telegram
from scrapy.settings import Settings
import scrapydo
import time

def crawler_reddit(subreddits):

    message = ''
    max = 10
    count = 0

    data = scrapydo.run_spider(RedditSpider(), settings=settings, subreddits=subreddits)

    for item in data:
        count += 1

        if item["title"] == '':
            title = "_No Title_ :("
        else:
            title = item["title"]

        message += "*" + item["subreddit"] + "*, votes " + str(item["upvote"]) + " " + "[" + title + "](" + \
                   item["thread_link"] + ") \n"
        if count > max:
            break
    if len(data) == 0:
        message = "Desculpe, não há nenhum tópico quente nestes seus reddits :("
    return message


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Olá, seja bem vindo ao Challenge idW bot.")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def nada_pra_fazer(bot, update, args):
    arg = ' '.join(args).upper()
    if arg == '':
        bot.send_message(chat_id=update.message.chat_id, text="Por favor, informe a lista de subreddits que quer ver, assim /nadaprafazer programming;dogs;brazil")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Vou buscar diretamente no Reddit estas informações. Isso deve levar uns minutos...")
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING, timeout=120)
        json_return = crawler_reddit(arg)
        bot.send_message(chat_id=update.message.chat_id, text=json_return, parse_mode=telegram.ParseMode.MARKDOWN)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Desculpe, não te entendi :(")


scrapydo.setup()

settings = Settings()
settings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
settings.set("FEED_FORMAT", "json")
settings.set("FEED_URI", "result.json")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='497792629:AAHb-vEAOvjeocP8D_8z0Imxuorb1F6tiW4')
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

npfz_handler = CommandHandler('nadaprafazer', nada_pra_fazer, pass_args=True)
dispatcher.add_handler(npfz_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Para manter ativo a Thread Principal, do contrário, o controle de threads do Scrapy
# não consegue reativar crawler sob-demanda.
# Em um ambiente de produção, os crawlers seriam consumidos por API por algum Daemon, como
# por exemplo o Scrapyd.

while True:
    time.sleep(60)