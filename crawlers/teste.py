from bs4 import BeautifulSoup
import urllib

req = urllib.request.Request(url="https://www.reddit.com/r/AskReddit/",headers={'User-agent': 'tester 0.2'})

page = urllib.request.urlopen(req).read()
soup = BeautifulSoup(page, "lxml")
conteudo = soup.prettify()

lista = soup.find("div", {"id": "siteTable"})

dados_reddit = {}
lista_dados = []

for l in lista:
    #print(l)
    score = l.find("div", {"class": "score likes"})

    if score is not None:

        subreddit = l["data-subreddit"]
        comments_link = l.find("a", {"class": "bylink comments may-blank"})['data-href-url']
        thread_link = l.find("a", {"class": "bylink comments may-blank"})['href']
        title = l.a.text

        if score.text == '•' :
            upvote = 0
        else:
            upvote = score['title']

        dados_reddit["subreddit"] = subreddit
        dados_reddit["comments_link"] = comments_link
        dados_reddit["thread_link"] = thread_link
        dados_reddit["title"] = title
        dados_reddit["upvote"] = upvote

        lista_dados.append(dados_reddit)

print(lista_dados)
