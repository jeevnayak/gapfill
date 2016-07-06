import json
import wikipedia

ARTICLES_TO_FETCH = [
    "George W. Bush",
    "United States",
    "Barack Obama",
    "World War II",
    "Catholic Church",
    "The Beatles",
    "India",
    "Facebook",
    "Google",
    "Justin Bieber",
    "Steve Jobs",
    "Star Wars",
    "Kanye West",
    "Donald Trump",
    "Game of Thrones",
    "Michael Jordan",
]

if __name__ == '__main__':
    # fetch the text of each article from Wikipedia
    articles = []
    for article_title in ARTICLES_TO_FETCH:
        # note: we're just fetching the summary at the top of each articla
        article_text = wikipedia.summary(article_title)
        articles.append({
            "title": article_title,
            "text": article_text,
            })

    # write the articles to a json file that can be parsed by wiki_parser.py
    with open("outputs/wiki_articles.json", "w") as outfile:
        json.dump(articles, outfile)

    print "Wrote articles to outputs/wiki_articles.json"
