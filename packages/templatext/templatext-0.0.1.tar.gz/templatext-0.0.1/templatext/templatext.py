import re
import string

import spacy
import unidecode
import gensim.downloader as api

from word2number import w2n
from bs4 import BeautifulSoup

from contractions import expand_contractions

# nlp = spacy.load('en_core_web_md')

example = """<h1 id="i-what-is-preprocessing">I. What is preprocessing?</h1>

<p>Preprocessing in Natural Language Processing (NLP) is the process by which we try to “standardize” the text we want to analyze.</p>

<p>A challenge that arises pretty quickly when you try to build an efficient preprocessing NLP pipeline is the diversity of the texts you might deal with :</p>
<ul>
  <li>tweets that would be highly informal</li>
  <li>cover letters from candidates in an HR company</li>
  <li>Slack messages within a team</li>
  <li>Even code sometimes if you try to analyze Github comments for example</li>
</ul>

<p>The diversity makes the whole thing tricky. Usually, a given pipeline is developed for a certain kind of text. The pipeline should give us a “clean” text version.</p>

<p>Another challenge that arises when dealing with text preprocessing is the language. The English language remains quite simple to preprocess. German or french use for example much more special characters like “é, à, ö, ï”.</p>

<p>You might now wonder what are the main steps of preprocessing?</p>
<ul>
  <li>A first step is to remove words that are made of special characters (if needed in your case): <code class="language-plaintext highlighter-rouge">@,#, /,!.\'+-= </code></li>
  <li>In English, some words are short versions of actuals words, e.g “I’m” for “I am”. To treat them as separate words, you’ll need to split them.</li>
  <li>We then would like to remove specific syntax linked to our text extraction, e.g “\n” every time there is a new line</li>
  <li>Remove the stop words, which are mainstream words like “the, I, would”…</li>
  <li>Once this step is done, we are ready to tokenize the text, i.e split by word</li>
  <li>To make sure that the words “Shoe” and “shoe” are later understood as the same, lower case the tokens</li>
  <li>Lemmatize the tokens to extract the “root” of each word.</li>
</ul>"""

punctuation_regex = re.compile("[%s]" % re.escape(string.punctuation))

class Templatext:
    def __init__(self, language="en", remove_html=True, extra_whitespace=True,
                accented_chars=True, contractions=True, lowercase=True, stop_words=True,
                punctuations=True, special_chars=True, remove_num=True, convert_num=True,
                lemmatization=True, punctuation=True, tokens=True):
        self.language = language
        self.remove_html = remove_html
        self.extra_whitespace = extra_whitespace
        self.accented_chars = accented_chars
        self.contractions = contractions
        self.lowercase = lowercase
        self.stop_words = stop_words
        self.punctuations = punctuations
        self.special_chars = special_chars
        self.remove_num = remove_num
        self.convert_num = convert_num
        self.lemmatization = lemmatization
        self.punctuation = punctuation
        self.tokens = tokens

        self.nlp = spacy.load('en_core_web_md')

    @staticmethod
    def strip_html_tags(text):
        """Remove HTML tags from text"""
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    @staticmethod
    def remove_whitespace(text):
        """Remove extra whitespaces from text"""
        text = text.strip()
        return " ".join(text.split())
    
    @staticmethod
    def remove_accented_chars(text):
        """Remove accented characters from text, e.g. café"""
        text = unidecode.unidecode(text)
        return text
    
    @staticmethod
    def lower(text):
        """Convert text to lowercase"""
        return text.lower()

    @staticmethod
    def expand_contractions(text):
        """Expand contracted words, e.g. don't to do not"""
        text = expand_contractions(text)
        return text

    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from text"""
        return punctuation_regex.sub("", text)

    def preprocess(self, text):
        """Perform text preprocessing"""
        if self.remove_html:
            text = self.strip_html_tags(text)
        if self.extra_whitespace:
            text = self.remove_whitespace(text)
        if self.accented_chars:
            text = self.remove_accented_chars(text)
        if self.contractions:
            text = self.expand_contractions(text)
        if self.lowercase:
            text = self.lower(text)
        if self.punctuation:
            text = self.remove_punctuation(text)

        doc = self.nlp(text)
        clean_text = []

        for token in doc:
            flag = True
            edit = token.text
            if self.stop_words and token.is_stop and token.pos_ != 'NUM':
                flag = False
            if self.punctuations and token.pos_ == 'PUNCT' and flag:
                flag = False
            if self.special_chars and token.pos_ == 'SYM' and flag:
                flag = False
            if self.remove_num and (token.pos_ == 'NUM' or token.text.isnumeric()) and flag:
                flag = False
            if self.convert_num and token.pos_ == 'NUM' and flag:
                edit = w2n.word_to_num(token.text)
            elif self.lemmatization and token.lemma_ != "-PRON-" and flag:
                edit = token.lemma_
            if edit.strip() != "" and flag:
                clean_text.append(edit)

        return clean_text
        
