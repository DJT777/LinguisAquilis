import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
from scipy.sparse import csr_matrix

class TFIDF:

    def compute_cosine_similarity(self, a, b):
        """Compute the cosine similarity between two 1D numpy arrays."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        cosine_sim = dot_product / (norm_a * norm_b)
        return cosine_sim

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.type = 'TFIDF'
        self.class_json = open('notebooks/USE-BERT-BOW-Word2Vec-TFIDF-GLOVE-OpenAI-ELMO-cleaned.json')
        self.class_data = json.load(self.class_json)
        self.corpus = [course['course_description'] for course in self.class_data]
        self.fit(self.corpus)

    def fit(self, documents):
        self.vectorizer.fit(documents)

    def embed(self, text):
        text = text[0]
        return self.vectorizer.transform([text])

    def compare(self, input_embedding, dict_list):
        # Convert the input embedding to a dense NumPy array
        if isinstance(input_embedding, csr_matrix):
            input_embedding = input_embedding.toarray().tolist()

        input_embedding = np.array(input_embedding).reshape(1, -1)

        # Compare the input embedding with the TF-IDF embedding in each dictionary
        similarities = []
        for i, dictionary in enumerate(dict_list):
            tfidf_embedding = dictionary['TFIDF_embedding'][0]
            tfidf_array = np.array(tfidf_embedding).reshape(1, -1)
            #tfidf_shape = tfidf_array.shape

            # Pad the input and TF-IDF embeddings with zeros to have the same shape
            #max_features = max(input_shape[0], tfidf_shape[0])
            #padded_input = np.zeros((input_shape[0], max_features))
            #padded_tfidf = np.zeros((tfidf_shape[0], max_features))

            #padded_input[:, :input_shape[0]] = input_array
            #padded_tfidf[:, :tfidf_shape[0]] = tfidf_array

            # Compute the cosine similarity
            similarity = cosine_similarity(input_embedding, tfidf_array)[0][0]
            similarities.append((i, similarity))

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
