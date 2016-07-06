import nltk
import string

from keyword_chooser import KeywordChooser
from nltk.tokenize import WhitespaceTokenizer

# Weights applied to each sentence attribute when considering it as a fill in the blank candidate.
# Note: the pronoun weight is negative because more pronouns make a sentence a worse candidate.
SENTENCE_SCORE_WEIGHTS = {
    'first': 1,
    'title': 1,
    'superlative': 0.5,
    'length': 0.1,
    'noun': 0.1,
    'pronoun': -0.5,
}

# All sentences with a score higher than this threshold will be chosen as fill in the blank candidates.
SENTENCE_SCORE_THRESHOLD = 4

class SentenceChooser:
    """Class that chooses the sentences that are best suited for fill in the blank questions from a given list."""

    def __init__(self, title, sentences):
        self.title = title
        self.sentences = sentences

    def choose_best_sentences(self):
        """Returns a list of sentences in the article that are best suited for fill in the blank questions."""
        best_sentences = []
        for i, sentence in enumerate(self.sentences):
            if self._calculate_sentence_score(sentence, i) > SENTENCE_SCORE_THRESHOLD:
                best_sentences.append(sentence)
        return best_sentences

    def _calculate_sentence_score(self, sentence, sentence_index):
        """Calculates a score that reflects how good the given sentence would be as a fill in the blank question."""
        return (self._calculate_sentence_first_score(sentence_index) +
            self._calculate_sentence_title_score(sentence) +
            self._calculate_sentence_superlative_score(sentence) +
            self._calculate_sentence_length_score(sentence) +
            self._calculate_sentence_noun_score(sentence) +
            self._calculate_sentence_pronoun_score(sentence))

    def _calculate_sentence_first_score(self, sentence_index):
        """Calculates a score based on whether the sentence is the first one in the article."""
        score = 1 if sentence_index == 0 else 0
        return SENTENCE_SCORE_WEIGHTS['first'] * score

    def _calculate_sentence_title_score(self, sentence):
        """Calculates a score based on how many words the sentence shares with the article title."""
        title = self._remove_punctuation(self.title)
        sentence = self._remove_punctuation(sentence)
        tokenizer = WhitespaceTokenizer()
        tokenized_title = tokenizer.tokenize(title)
        tokenized_sentence = tokenizer.tokenize(sentence)
        
        common_words = set()
        for word in tokenized_sentence:
            if word in tokenized_title:
                common_words.add(word)

        score = float(len(common_words)) / len(tokenized_sentence)
        return SENTENCE_SCORE_WEIGHTS['title'] * score

    def _calculate_sentence_superlative_score(self, sentence):
        """Calculates a score based on whether the sentence contains at least one superlative."""
        score = 1 if self._num_pos_in_sentence(sentence, self._is_superlative) > 0 else 0
        return SENTENCE_SCORE_WEIGHTS['superlative'] * score

    def _calculate_sentence_length_score(self, sentence):
        """Calculates a score based on the length of the sentence."""
        score = len(WhitespaceTokenizer().tokenize(sentence))
        return SENTENCE_SCORE_WEIGHTS['length'] * score

    def _calculate_sentence_noun_score(self, sentence):
        """Calculates a score based on how many nouns are contained in the sentence."""
        score = self._num_pos_in_sentence(sentence, self._is_noun)
        return SENTENCE_SCORE_WEIGHTS['noun'] * score

    def _calculate_sentence_pronoun_score(self, sentence):
        """Calculates a score based on how many pronouns are contained in the sentence."""
        score = self._num_pos_in_sentence(sentence, self._is_pronoun)
        return SENTENCE_SCORE_WEIGHTS['pronoun'] * score

    def _num_pos_in_sentence(self, sentence, pos_function):
        """Counts the number of a certain part of speech in a sentence, using the given part of speech filter function."""
        tagged_tokens = nltk.pos_tag(nltk.word_tokenize(sentence))
        num_pos = 0
        for tagged_token in tagged_tokens:
            if pos_function(tagged_token[1]):
                num_pos += 1
        return num_pos

    def _remove_punctuation(self, text):
        """Returns a copy of the given text with punctuation removed."""
        for c in string.punctuation:
            text = text.replace(c, "")
        return text

    def _is_noun(self, pos_tag):
        """Returns whether the given part of speech tag represents a noun."""
        return pos_tag.startswith("N")

    def _is_pronoun(self, pos_tag):
        """Returns whether the given part of speech tag represents a pronoun."""
        return pos_tag.startswith("PRP")

    def _is_superlative(self, pos_tag):
        """Returns whether the given part of speech tag represents a superlative."""
        return pos_tag == "JJS" or pos_tag == "RBS"
