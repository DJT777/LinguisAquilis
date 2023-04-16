import openai
import numpy as np


class OpenAIEmbedding:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def encode(self, text):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text,
            max_tokens=512,
            n=1,
            stop=None,
            temperature=0.5,
        )

        embeddings = response.choices[0].embedding
        embeddings = np.asarray(embeddings).astype('float32')
        embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
