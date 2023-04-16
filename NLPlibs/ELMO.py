import tensorflow_hub as hub
import tensorflow as tf


def create_elmo_module():
    """
    Create an ELMO embedding module using TensorFlow Hub.

    Returns:
        module: The ELMO embedding module.
    """
    url = "https://tfhub.dev/google/elmo/3"
    return hub.Module(url, trainable=True)


def elmo_embeddings(module, sentences):
    """
    Compute ELMO embeddings for a list of sentences.

    Parameters:
        module (module): The ELMO embedding module.
        sentences (list): A list of strings representing the sentences to embed.

    Returns:
        np.ndarray: A numpy array of shape (num_sentences, embedding_dim) containing the embeddings for each sentence.
    """
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(tf.tables_initializer())
        embeddings = sess.run(module(sentences))
    return embeddings
