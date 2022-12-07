import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api
class GloVe:
    def __init__(self):
        self.model = api.load('glove-wiki-gigaword-300')
        self.type = 'glove'

    def encode(self, text):
        text = text[0]
        tokens = text.split()
        embeddings = []
        for token in tokens:
            if token in self.model:
                embeddings.append(self.model[token])
        if embeddings:
            return np.mean(embeddings, axis=0)
        else:
            return np.zeros(self.model.vector_size)


    def embed(self, text):
        embeddings = self.encode(text)
        return embeddings
        # Perform inference using the embeddings
        # Return the predicted output


    def compare(self, input_embedding, dict_list):
        similarities = []
        input_embedding = np.array(input_embedding)
        for i, dictionary in enumerate(dict_list):
            glove_embedding = np.array(dictionary['glove_embedding'])
            print("Glove Embedding size" + str(len(glove_embedding)))
            print("Compared to Embedding Size " + str(len(dictionary['glove_embedding'])))
            similarity = cosine_similarity(input_embedding.reshape(1, -1), glove_embedding.reshape(1, -1))[0]
            similarities.append((i, similarity))

        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        return sorted_similarities
