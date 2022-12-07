from transformers import BertTokenizer, TFBertModel
import tensorflow as tf
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.python.ops.numpy_ops import np_config

np_config.enable_numpy_behavior()

class BERT:
    def __init__(self, model_name):

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = TFBertModel.from_pretrained(model_name)
        self.type = 'BERT'

    def embed(self, text):
        model_name = 'bert-base-uncased'

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = TFBertModel.from_pretrained(model_name)
        self.type = 'BERT'

        # Tokenize input text
        inputs = self.tokenizer(text, return_tensors='tf', padding=True, truncation=True, max_length=512)

        # Get the BERT output
        outputs = self.model(inputs)

        # Extract the embeddings for each token
        embeddings = outputs.last_hidden_state

        # Calculate the mean of the token embeddings to obtain a single sentence embedding
        sentence_embedding = tf.reduce_mean(embeddings, axis=1)

        sentence_embedding = sentence_embedding.numpy()

        return sentence_embedding

    def compare(self, input_embedding, dict_list):
        # Compare the input embedding with the 'USE_embedding' key in each dictionary
        similarities = []
        input_embedding = input_embedding
        for i, dictionary in enumerate(dict_list):
            bertEmbedding = np.array(dictionary['BERT_embedding'])
            input_embedding = np.array(input_embedding)
            similarity = cosine_similarity(input_embedding.reshape(-1, 768), bertEmbedding.reshape(-1, 768))[0][0]
            print(similarity)
            similarities.append((i, similarity))

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
