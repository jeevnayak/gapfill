Fill in the Blank
=

A simple web app that presents the user with a series of fill in the blank questions. The code is divided into two parts: Python scripts that are used to automatically generate fill in the blank questions using Wikipedia articles, and a Node.js web app that presents those questions.

Installation
-

- Clone the repository
- Make sure you have Python and Node.js installed
- In the `parser` directory, run `pip install -r requirements.txt`
- To re-fetch the articles from Wikipedia, run `python wiki_fetcher.py`
- To regenerate the questions from the fetched articles, run `python wiki_parser.py`
- To use the new list of questions in the web app, copy `outputs/gapfill_questions.json` to the `app/data` directory
- In the `app` directory, run `npm install`
- Run `node app.js`
- Go to `localhost:3000` in your browser to try it out!

The Parser
-

The Wikipedia fetching and parsing code is in the `parser` directory. The fetching of article content is handled by `wiki_fetcher.py`, and the contents are stored in an output json file. The content parsing and question generation is handled by `wiki_parser.py`.

The high-level approach for question generation involves:

1. Downloading the content (just the summary section at the top) of each Wikipedia article listed in `wiki_fetcher.py`
2. Breaking up each article into sentences
3. Choosing the sentences that are best suited for fill in the blank questions
4. For each of those sentences, choosing the best word to blank out
5. Writing the questions to a json file that can be used by the web app

The approach for choosing sentences and keywords was mostly inspired by this paper: http://www.anthology.aclweb.org/W/W11/W11-1407.pdf. The best sentences are chosen based on the following criteria:

- Whether the sentence is the first sentence in the article
- The number of words that the sentence shares with the article title
- Whether the sentence contains at least one superlative
- The length of the sentence
- The number of nouns in the sentence
- The number of pronouns in the sentence (this is a negative signal)

Each chosen sentence is then broken down into noun phrases and one candidate word to blank out is chosen from each noun phrase. The best word is chosen from the candidate list based on how often that word appears in the article and whether it appears in the article title.

The App
-

The web app is a pretty simple Node.js app. All of the server code is in `app.js`, which parses the questions from the input json file and exposes endpoints for getting questions and checking answers. The client code is in the `static` directory, which includes Javascript that handles user input and fetches data from the server.
