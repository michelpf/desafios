# Crawler

## Introdução

Este _crawler_ foi desenvolvido em Python utilizando o framework [Scrapy](https://scrapy.org/).
Apesar de ser mais usado via linha de comando `scrapy`, foi criado dentro do _spider_ uma função 
que permite sua execução na própria IDE, como o PyCharm, programaticamente, podendo ter o seu 
uso estendido para outras aplicações, como APIs.

Para não criar muitas adaptações e utilizar os componentes próprios do Scrapy, foi utilizado,
como forma de saída dos dados, um arquivo JSON que fica na pasta do respectivo _spider_.

## Modo de uso

Abrir o arquivo **reddit.py** em `crawlers/scrap_reddit/spiders`.
Na função main, editar a lista de subreddits pela variável **subreddits**.

```python
if __name__ == '__main__':

    subreddits = "askreddit;worldnews;cats"

    if os.path.exists("result.json"):
        os.remove("result.json")

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json'
    })


    process.crawl(RedditSpider, subreddits=subreddits)
    process.start()
```

Ao final da execução do crawler é gerado um arquivo de saída em JSON.
Abaixo segue um exemplo de saída do arquivo.

A cada nova execução do spider um novo arquivo é gerado, sobrescrevendo o anterior.

```json
[
{"subreddit": "worldnews", "comments_link": "/r/worldnews/comments/7ez1rb/right_for_all_to_access_the_internet_is/", "thread_link": "https://www.reddit.com/r/worldnews/comments/7ez1rb/right_for_all_to_access_the_internet_is/", "title": "Right for all to access the internet is \u2018non-negotiable\u2019, says Indian Minister for Law & Information Technology at global cyberspace meet", "upvote": 55909},
{"subreddit": "worldnews", "comments_link": "/r/worldnews/comments/7ezxt0/manafort_flight_records_show_deeper_kremlin_ties/", "thread_link": "https://www.reddit.com/r/worldnews/comments/7ezxt0/manafort_flight_records_show_deeper_kremlin_ties/", "title": "Manafort flight records show deeper Kremlin ties than previously known", "upvote": 5358},
{"subreddit": "worldnews", "comments_link": "/r/worldnews/comments/7eyspr/uk_officially_falls_out_of_worlds_top_five/", "thread_link": "https://www.reddit.com/r/worldnews/comments/7eyspr/uk_officially_falls_out_of_worlds_top_five/", "title": "UK officially falls out of world\u2019s top five economies, Government admits", "upvote": 11251},
{"subreddit": "AskReddit", "comments_link": "/r/AskReddit/comments/7ez0aq/what_is_embarrassing_to_do_alone_but_fun_to_do_in/", "thread_link": "https://www.reddit.com/r/AskReddit/comments/7ez0aq/what_is_embarrassing_to_do_alone_but_fun_to_do_in/", "title": "What is embarrassing to do alone but fun to do in groups?", "upvote": 26021},
{"subreddit": "AskReddit", "comments_link": "/r/AskReddit/comments/7ez41n/police_officers_of_reddit_whats_the_oddest_place/", "thread_link": "https://www.reddit.com/r/AskReddit/comments/7ez41n/police_officers_of_reddit_whats_the_oddest_place/", "title": "Police officers of Reddit, what's the oddest place you've encountered people you formerly arrested?", "upvote": 6095},
{"subreddit": "worldnews", "comments_link": "/r/worldnews/comments/7exgh6/trump_exposed_covert_israeli_commando_raid_deep/", "thread_link": "https://www.reddit.com/r/worldnews/comments/7exgh6/trump_exposed_covert_israeli_commando_raid_deep/", "title": "Trump exposed covert Israeli commando raid deep in Syria to Russia", "upvote": 33594}
```
Também é possível executar por linha de comando o arquivo cli_cralwer, passando como argumento
o comando -s seguido da lista de subreddit para buscar. Neste script foi utilizado a 
biblioteca _Scrapydo_ por sua simplicidade no retorno dos itens de execução do _spider_.

`cli_cralwer -s programming;cats;dogs`

O resultado apresentado é o seguinte:

```
Iniciando crawler para buscar dados dos subreddits askreddit...
AskReddit, votes 19415 [What is an album where EVERY song is good?](https://www.reddit.com/r/AskReddit/comments/7f7p7q/what_is_an_album_where_every_song_is_good/) 

AskReddit, votes 6886 [What things do we do today that people 50 or 60 years ago would think is absolutely ridiculous?](https://www.reddit.com/r/AskReddit/comments/7f7tel/what_things_do_we_do_today_that_people_50_or_60/) 

AskReddit, votes 5701 [What Are Your Movie Theater Pro Tips?](https://www.reddit.com/r/AskReddit/comments/7f7zth/what_are_your_movie_theater_pro_tips/) 

AskReddit, votes 6204 [What's the most interesting Wikipedia page you've ever read?](https://www.reddit.com/r/AskReddit/comments/7f7r37/whats_the_most_interesting_wikipedia_page_youve/) 

AskReddit, votes 18699 [What is your current obsession?](https://www.reddit.com/r/AskReddit/comments/7f75k7/what_is_your_current_obsession/) 
```

# Telegram Chatbot

## Introdução

Este _chatbot_ foi desenvolvido em Python utilizando o framework [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot).
Sua implementação é bem simples, sendo configurado as seguintes ações:

1. start ou saudação, quando alguém entra no chatbot;
2. comando nadaprafazer, que inicia uma crawler sob-demanda com a lista de subreddits desejados;
3. comando não reconheci, quando o usuário entra com um comando não esperado.

O usuário criado é [idw_reddit_bot](tg://resolve?domain=idw_reddit_bot).

Como o _Scrapy_ possui um controle de threads (_reactors_) separado do controle de threads que a API do Telegram
utiliza, houve certa dificuldade para a execução sob-demanda.
Para solucionar esta condição, nesta prova de conceito, foi incluído uma âncora no script do 
chatbot para manter a thread principal ativa.

Com efeito, a biblioeca [Scrapydo](https://github.com/rmax/scrapydo), consegue criar um ambiente 
controlado de processado via o componente _Crochet_, permitindo assim a execução sob-demanda indefinidamente.

## Modo de uso

Entrar no bot pelo link do usuário, e enviar o comando /nadaprafazer seguido da lista de 
subreddits separados por ponto-e-vírgula.

![Imagem do Chatbot](crawlers/bot_image.png)