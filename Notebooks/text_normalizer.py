from neattext.functions import clean_text
import nltk
import spacy
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download("stopwords")


tokenizer_0 = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')
nlp = spacy.load('en_core_web_sm')

def stem_text(text):
    porter = PorterStemmer()
    words = tokenizer_0.tokenize(text) 
    stem_sentence=[]
    for word in words:
        stem_sentence.append(porter.stem(word))
    port = " ".join(stem_sentence)

    return port

def lemmatize_text(text):
    doc = nlp(text)
    lemma_sentence = []
    for token in doc:
        lemma_sentence.append(token.lemma_)
    lemma = " ".join(lemma_sentence)

    return lemma