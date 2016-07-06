import json
import nltk

from keyword_chooser import KeywordChooser
from sentence_chooser import SentenceChooser

def setup_dependencies():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

def split_text_into_sentences(text):
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return sentence_tokenizer.tokenize(text.strip())

if __name__ == '__main__':
    setup_dependencies()

    # read in the article data downloaded by wiki_fetcher.py
    articles = []
    with open("outputs/wiki_articles.json", "r") as infile:
        articles = json.load(infile)

    # build up a list of fill in the blank questions
    sentences_and_keywords = []
    for article in articles:
        article_title = article["title"]
        article_text = article["text"]
        sentences = split_text_into_sentences(article_text)

        # find the sentences from the article that are most suited to be a fill in the blank
        sentence_chooser = SentenceChooser(article_title, sentences)
        best_sentences = sentence_chooser.choose_best_sentences()

        # find the best word in each sentence to blank out
        for sentence in best_sentences:
            keyword_chooser = KeywordChooser(article_title, article_text, sentence)
            keyword = keyword_chooser.choose_keyword()
            if keyword:
                sentences_and_keywords.append({
                    "sentence": sentence,
                    "keyword": keyword
                    })

    # write the resulting questions into an output json file
    with open("outputs/gapfill_questions.json", "w") as outfile:
        json.dump(sentences_and_keywords, outfile)

    print "Wrote questions to outputs/gapfill_questions.json"
