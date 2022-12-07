import openai
import numpy as np
from openai.embeddings_utils import get_embedding
from typing import List



# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191



class OpenAI:
    def __init__(self, api_key):
        self.api_key = "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"
        openai.api_key = self.api_key
        self.type = 'OpenAI'


    def embed(self, text: str) -> List[float]:
        model = "text-embedding-ada-002"
        embedding = openai.Embedding.create(input=[text[0]], model=model)["data"][0]["embedding"]
        return embedding

    def compute_cosine_similarity(self, a, b):
        """Compute the cosine similarity between two 1D numpy arrays."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        cosine_sim = dot_product / (norm_a * norm_b)
        return cosine_sim


    def compare(self, input_embedding, dict_list):

        # Compare the input embedding with the TF-IDF embedding in each dictionary
        similarities = []
        for i, dictionary in enumerate(dict_list):
            input_embed = input_embedding
            openai_embedding = dictionary['OpenAI_embedding']
            similarity = self.compute_cosine_similarity(input_embed, openai_embedding)
            similarities.append((i, similarity))

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities