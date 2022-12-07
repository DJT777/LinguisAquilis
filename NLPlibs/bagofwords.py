from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class BagOfWords:
    def __init__(self, stop_words='english', max_features=None):
        self.vectorizer = CountVectorizer(stop_words=stop_words, max_features=max_features)
        self.vocab = None
        self.embeddings = None
        self.type = 'BagOfWords'
        self.class_json = open('notebooks/USE-BERT-BOW-Word2Vec-TFIDF-GLOVE-OpenAI-ELMO-cleaned.json')
        self.class_data = json.load(self.class_json)
        self.corpus = [course['course_description'] for course in self.class_data]
        self.fit(self.corpus)
        self.type = "BagOfWords"

    def compute_cosine_similarity(self, a, b):
        """Compute the cosine similarity between two 1D numpy arrays."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        cosine_sim = dot_product / (norm_a * norm_b)
        return cosine_sim

    def fit(self, sentences):
        self.embeddings = self.vectorizer.fit_transform(sentences)
        self.vocab = self.vectorizer.vocabulary_

    def embed(self, text):
        text = text[0]
        return self.vectorizer.transform([text]).toarray()

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output


    def compare(self, input_embedding, dict_list):

        # Compare the input embedding with the TF-IDF embedding in each dictionary
        similarities = []
        for i, dictionary in enumerate(dict_list):
            input_embed = input_embedding[0]
            bow_embedding = dictionary['BagOfWords_embedding'][0]
            max_length = max(len(input_embed), len(bow_embedding))

            new_embedding1 = np.zeros(max_length)
            new_embedding2 = np.zeros(max_length)

            new_embedding1[:len(input_embed)] = input_embed
            new_embedding2[:len(bow_embedding)] = bow_embedding

            similarity = cosine_similarity(new_embedding1.reshape(1, -1), new_embedding2.reshape(1, -1))
            similarities.append((i, similarity))

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities