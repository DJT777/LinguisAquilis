import numpy as np
import urllib.request
import io

#embeddings, index_to_word = load_glove_embeddings("http://nlp.stanford.edu/data/glove.6B.50d.txt", num_embeddings=10000)

def load_glove_embeddings(path, num_embeddings=None):
    """
    Load GloVe embeddings from a file.

    Parameters:
        path (str): The URL to the GloVe file.
        num_embeddings (int): The number of embeddings to load. If None, load all embeddings.

    Returns:
        tuple: A tuple containing the following:
            - A numpy array of shape (vocab_size, embedding_dim) containing the embeddings.
            - A list containing the words corresponding to each row in the embeddings matrix.
    """
    word_to_index = {}
    index_to_word = []
    embeddings = []

    with urllib.request.urlopen(path) as f:
        for i, line in enumerate(io.TextIOWrapper(f)):
            if num_embeddings is not None and i >= num_embeddings:
                break
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_to_index[word] = len(index_to_word)
            index_to_word.append(word)
            embeddings.append(coefs)

    return np.array(embeddings), index_to_word
