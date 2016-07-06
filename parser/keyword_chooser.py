import nltk

# Weights applied to each keyword attribute when considering it as a blank-out candidate.
KEYWORD_SCORE_WEIGHTS = {
    'frequency': 1,
    'title': 1,
}

class KeywordChooser:
    """Class that chooses the best word to blank out from a given sentence for a fill in the blank question."""

    def __init__(self, title, full_text, sentence):
        self.title = title
        self.sentence = sentence
        # map of word -> number of times it appears in the full article text
        self.full_text_word_frequencies = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(full_text))
        # map of word -> number of times it appears in the given sentence
        self.sentence_word_frequencies = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(sentence))

    def choose_keyword(self):
        """Returns the best word to blank out in the sentence (can be None if no good ones are found)."""
        keyword_list = self._generate_keyword_list()
        return self._choose_keyword_from_list(keyword_list)

    def _generate_keyword_list(self):
        """Generates a list of keyword candidates from the sentence."""
        tagged_tokens = nltk.pos_tag(nltk.word_tokenize(self.sentence))

        # if there is a cardinal number in the sentence, immediately choose it as the keyword
        for word, pos_tag in tagged_tokens:
            if self._is_cardinal(pos_tag):
                return [word]

        # find all of the noun phrases (e.g. "the blue house") in the sentence
        noun_phrase_grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
        parse_tree = nltk.RegexpParser(noun_phrase_grammar).parse(tagged_tokens)
        noun_phrases = [subtree.leaves() for subtree in parse_tree.subtrees() if subtree.label() == "NP"]

        # choose zero or one word from each noun phrase as a keyword candidate
        keyword_list = []
        for noun_phrase in noun_phrases:
            best_keyword = self._choose_best_keyword_in_noun_phrase(noun_phrase)
            if best_keyword:
                keyword_list.append(best_keyword)

        return keyword_list

    def _choose_best_keyword_in_noun_phrase(self, noun_phrase):
        """Returns the best keyword candidate in the given noun phrase. This will be either the first adjective,
            or the first noun if there are no adjectives. Words that appear more than once in the sentence are ruled out."""
        first_noun = None
        for word, pos_tag in noun_phrase:
            if self.sentence_word_frequencies[word.lower()] > 1:
                continue

            if self._is_adjective(pos_tag):
                return word

            if self._is_noun(pos_tag) and first_noun is None:
                first_noun = word

        return first_noun

    def _choose_keyword_from_list(self, keyword_list):
        """Returns the best blank-out candidate from the given list, or None if the list is empty."""
        best_keyword = None
        best_keyword_score = 0
        for keyword in keyword_list:
            keyword_score = self._calculate_keyword_score(keyword)
            if keyword_score > best_keyword_score:
                best_keyword = keyword
                best_keyword_score = keyword_score

        return best_keyword

    def _calculate_keyword_score(self, keyword):
        """Calculates a score that reflects how good the given word would be to blank out."""
        return (self._calculate_keyword_frequency_score(keyword) +
            self._calculate_keyword_title_score(keyword))

    def _calculate_keyword_frequency_score(self, keyword):
        """Calculates a score based on how many times the word appears in the full article."""
        score = self.full_text_word_frequencies[keyword.lower()]
        return KEYWORD_SCORE_WEIGHTS['frequency'] * score

    def _calculate_keyword_title_score(self, keyword):
        """Calculates a score based on whether the word is also in the article title."""
        score = 1 if keyword in nltk.word_tokenize(self.title) else 0
        return KEYWORD_SCORE_WEIGHTS['title'] * score

    def _is_cardinal(self, pos_tag):
        """Returns whether the given part of speech tag represents a cardinal number."""
        return pos_tag == "CD"

    def _is_adjective(self, pos_tag):
        """Returns whether the given part of speech tag represents an adjective."""
        return pos_tag.startswith("JJ")

    def _is_noun(self, pos_tag):
        """Returns whether the given part of speech tag represents a noun."""
        return pos_tag.startswith("N")
