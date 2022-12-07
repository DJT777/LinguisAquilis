import numpy as np
from gensim.models import Word2Vec
import json
import numpy as np
from gensim.models import Word2Vec
import json

class Word2VecModel:
    def __init__(self, model_path=None, vector_size=512, window=5, min_count=5, workers=4):
        if model_path is not None:
            self.model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
        else:
            self.model = None
            self.vector_size = vector_size
            self.window = window
            self.min_count = min_count
            self.workers = workers
            self.class_json = open('notebooks/USE-BERT-BOW-Word2Vec-TFIDF-GLOVE-OpenAI-ELMO-cleaned.json')
            self.class_data = json.load(self.class_json)
            self.corpus = [course['course_description'] for course in self.class_data]
            self.fit(self.corpus)
            self.type = 'word2vec'

    def compute_cosine_similarity(self, a, b):
        """Compute the cosine similarity between two 1D numpy arrays."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        cosine_sim = dot_product / (norm_a * norm_b)
        return cosine_sim

    def fit(self, corpus):
        sentences = [doc.split() for doc in corpus]
        self.model = Word2Vec(sentences, vector_size=self.vector_size, window=self.window, min_count=self.min_count, workers=self.workers)

    def embed(self, text):
        text = text[0]
        tokens = text.split()
        embeddings = []
        for token in tokens:
            if token in self.model.wv.key_to_index:
                embeddings.append(self.model.wv[token])
        if embeddings:
            return np.mean(embeddings, axis=0)
        else:
            return np.zeros(self.vector_size)

    def compare(self, input_embedding, dict_list):
        # Compare the input embedding with the Word2Vec embeddings in each dictionary
        similarities = []
        for i, dictionary in enumerate(dict_list):
            if isinstance(input_embedding, np.ndarray):
                input_embedding = input_embedding.tolist()
            word2vec_embedding = dictionary['word2vec_embedding']
            similarity = self.compute_cosine_similarity(input_embedding, word2vec_embedding)
            similarities.append((i, similarity))

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities

    def predict(self, text):
        embedding = self.encode(text)
        # Perform inference using the embedding
        # Return the predicted output
