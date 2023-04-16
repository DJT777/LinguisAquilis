from sklearn.feature_extraction.text import CountVectorizer


class BagOfWords:
    def __init__(self, stop_words='english', max_features=None):
        self.vectorizer = CountVectorizer(stop_words=stop_words, max_features=max_features)
        self.vocab = None
        self.embeddings = None

    def fit(self, sentences):
        self.embeddings = self.vectorizer.fit_transform(sentences)
        self.vocab = self.vectorizer.get_feature_names()

    def encode(self, text):
        tokens = text.split()
        embeddings = [0] * len(self.vocab)
        for token in tokens:
            if token in self.vocab:
                embeddings[self.vocab.index(token)] += 1
        return embeddings

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
