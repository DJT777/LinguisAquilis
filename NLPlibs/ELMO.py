import tensorflow.compat.v1 as tf_compat
import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

tf_compat.disable_eager_execution()
tf_compat.reset_default_graph()

class ELMo:
    def __init__(self, model_url):
        self.graph = tf_compat.Graph()
        with self.graph.as_default():
            self.session = tf_compat.Session()
            self.model = hub.Module(model_url, trainable=True)
            self.session.run(tf_compat.global_variables_initializer())
            self.session.run(tf_compat.tables_initializer())
        self.type = 'ELMO'

    def embed(self, sentences):
        with self.graph.as_default():
            embeddings = self.model(sentences, signature="default", as_dict=True)["elmo"]
            mean_embeddings = tf_compat.reduce_mean(embeddings, axis=1)
            return self.session.run(mean_embeddings)

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output


    def compare(self, input_embedding, dict_list):
        # Compare the input embedding with the 'USE_embedding' key in each dictionary
        similarities = []
        input_embedding = np.array(input_embedding)
        for i, dictionary in enumerate(dict_list):
            try:
                use_embedding = np.array(dictionary['ELMO_embedding'])
                similarity = cosine_similarity(input_embedding.reshape(-1, 512), use_embedding.reshape(-1, 512))[0][0]
                print(similarity)
                similarities.append((i, similarity))
            except:
                continue

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities
