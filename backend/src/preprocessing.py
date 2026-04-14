import re

# synonym dictionary
SYNONYMS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "js": "javascript",
    "node": "nodejs",
    "react.js": "react",
    "mongo": "mongodb"
}


def clean_text(text):
    """
    Remove special characters and lowercase text
    """
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = text.lower()
    return text


def normalize_synonyms(text):
    """
    Replace synonyms with canonical skill names
    """
    words = text.split()

    normalized = []

    for word in words:
        if word in SYNONYMS:
            normalized.append(SYNONYMS[word])
        else:
            normalized.append(word)

    return " ".join(normalized)


def generate_ngrams(words, n=3):
    """
    Generate 1-gram, 2-gram, 3-gram phrases
    """
    ngrams = []

    for i in range(len(words)):
        for j in range(1, n+1):
            if i + j <= len(words):
                ngrams.append(" ".join(words[i:i+j]))

    return ngrams


def preprocess_text(text):

    text = clean_text(text)
    text = normalize_synonyms(text)

    words = text.split()
    ngrams = generate_ngrams(words)

    return words, ngrams