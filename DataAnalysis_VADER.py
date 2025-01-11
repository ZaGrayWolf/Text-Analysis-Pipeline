import os
import re
import string
import nltk
import ssl
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from openpyxl import Workbook
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# SSL workaround for NLTK data download
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Force download of necessary NLTK data
nltk.download('stopwords', force=True)
nltk.download('punkt', force=True)

# Set up stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuations = string.punctuation

# Initialize VADER sentiment intensity analyzer
analyzer = SentimentIntensityAnalyzer()

# Functions for analysis
def clean_text(text):
    """Remove stopwords and punctuations from the text."""
    tokens = word_tokenize(text.lower())
    return [word for word in tokens if word not in stop_words and word not in punctuations]

def syllable_count(word):
    word = word.lower()
    count = sum(1 for char in word if char in "aeiou")
    if word.endswith(('es', 'ed')) and len(word) > 2:
        count -= 1
    return max(count, 1)

def analyze_text(text):
    try:
        sentences = sent_tokenize(text, language='english')
    except LookupError as e:
        print(f"Error during sentence tokenization: {e}")
        sentences = []  # Fall back to empty list if tokenization fails

    words = clean_text(text)
    word_count = len(words)
    sentence_count = len(sentences)
    syllables_per_word = sum(syllable_count(word) for word in words) / word_count if word_count else 0
    complex_word_count = sum(1 for word in words if syllable_count(word) > 2)
    avg_sentence_length = word_count / sentence_count if sentence_count else 0
    percentage_complex_words = complex_word_count / word_count if word_count else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_word_length = sum(len(word) for word in words) / word_count if word_count else 0

    # VADER Sentiment Analysis
    sentiment = analyzer.polarity_scores(text)
    positive_score = sentiment['pos']
    negative_score = sentiment['neg']
    polarity_score = sentiment['compound']
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)  # Adjust subjectivity if needed
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.IGNORECASE))

    return {
        "Positive Score": positive_score,
        "Negative Score": negative_score,
        "Polarity Score": polarity_score,
        "Subjectivity Score": subjectivity_score,
        "Average Sentence Length": avg_sentence_length,
        "Percentage of Complex Words": percentage_complex_words,
        "Fog Index": fog_index,
        "Average Number of Words Per Sentence": avg_sentence_length,
        "Complex Word Count": complex_word_count,
        "Word Count": word_count,
        "Syllables Per Word": syllables_per_word,
        "Personal Pronouns": personal_pronouns,
        "Average Word Length": avg_word_length,
    }

input_folder = '/Users/abhudaysingh/Documents/PyCharm_Projects/Blackcoffer/BlackCoffer_Project/data'  # Update this path
output_excel = '/Users/abhudaysingh/Documents/PyCharm_Projects/Blackcoffer/BlackCoffer_Project/Output Data Structure (1).xlsx'  # Update this path

workbook = Workbook()
sheet = workbook.active
sheet.append([
    "URL_ID", "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
    "Average Sentence Length", "Percentage of Complex Words", "Fog Index",
    "Average Number of Words Per Sentence", "Complex Word Count", "Word Count",
    "Syllables Per Word", "Personal Pronouns", "Average Word Length"
])

for file in Path(input_folder).glob("*.txt"):
    url_id = file.stem
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    analysis = analyze_text(text)
    sheet.append([
        url_id, analysis["Positive Score"], analysis["Negative Score"], analysis["Polarity Score"],
        analysis["Subjectivity Score"], analysis["Average Sentence Length"],
        analysis["Percentage of Complex Words"], analysis["Fog Index"],
        analysis["Average Number of Words Per Sentence"], analysis["Complex Word Count"],
        analysis["Word Count"], analysis["Syllables Per Word"], analysis["Personal Pronouns"],
        analysis["Average Word Length"]
    ])

workbook.save(output_excel)
print(f"Analysis complete. Results saved to {output_excel}")
