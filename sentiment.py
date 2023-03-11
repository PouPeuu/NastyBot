import emoji.unicode_codes
import text2emotion
import nltk
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download([
  "names",
  "stopwords",
  "state_union",
  "twitter_samples",
  "movie_reviews",
  "averaged_perceptron_tagger",
  "vader_lexicon",
  "punkt",
])

nlp = spacy.load("en_core_web_sm")

sia = SentimentIntensityAnalyzer()


def get_subject_phrase(doc):
  for token in doc:
    if ("subj" in token.dep_):
      subtree = list(token.subtree)
      start = subtree[0].i
      end = subtree[-1].i + 1
      return doc[start:end]


def get_object_phrase(doc):
  for token in doc:
    if ("dobj" in token.dep_):
      subtree = list(token.subtree)
      start = subtree[0].i
      end = subtree[-1].i + 1
      return doc[start:end]


while (True):
  print("start")
  x = input()
  text = x
  sentiment_phrase = sia.polarity_scores(x)
  doc = nlp(x)
  subject_phrase = get_subject_phrase(doc)
  object_phrase = get_object_phrase(doc)
  emotion_phrase = text2emotion.get_emotion(text)
  print(sentiment_phrase)
  print("Subject: " + str(subject_phrase))
  print("Object: " + str(object_phrase))
  print(emotion_phrase)
  subject_phrase = subject_phrase
  emotion_phrase = emotion_phrase
  sent_neg = sentiment_phrase["neg"]
  sent_neu = sentiment_phrase["neu"]
  sent_pos = sentiment_phrase["pos"]
  sent_comp = sentiment_phrase["compound"]
  emot_hap = emotion_phrase["Happy"]
  emot_ang = emotion_phrase["Angry"]
  emot_sur = emotion_phrase["Surprise"]
  emot_sad = emotion_phrase["Sad"]
  emot_fear = emotion_phrase["Fear"]