from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np


class Word2VecEmbedding:
    def __init__(self, sentences=None, vector_size=100, window=5, min_count=5):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.vocab = None
        self.embeddings = None
        if sentences:
            self.fit(sentences)

    def fit(self, sentences):
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), min_df=self.min_count, window=self.window)
        X = vectorizer.fit_transform(sentences)
        self.vocab = vectorizer.get_feature_names()
        svd = TruncatedSVD(n_components=self.vector_size)
        self.embeddings = svd.fit_transform(X)
        self.embeddings /= np.linalg.norm(self.embeddings, axis=1, keepdims=True)

    def encode(self, text):
        tokens = text.split()
        embeddings = []
        for token in tokens:
            if token in self.vocab:
                embeddings.append(self.embeddings[self.vocab.index(token)])
        return embeddings

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
