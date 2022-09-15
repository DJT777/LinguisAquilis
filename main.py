from flask import Flask, render_template, request
from absl import logging

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import tensorflow_hub as hub
import sentencepiece as spm
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import hnswlib
import json

app = Flask(__name__)
class_json = open('data.json')
class_data = json.load(class_json)

def create_embeddings(userInput):
    module = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-lite/2")
    input_placeholder = tf.sparse_placeholder(tf.int64, shape=[None, None])
    encodings = module(
        inputs=dict(
            values=input_placeholder.values,
            indices=input_placeholder.indices,
            dense_shape=input_placeholder.dense_shape))

    with tf.Session() as sess:
        spm_path = sess.run(module(signature="spm_path"))

    sp = spm.SentencePieceProcessor()
    with tf.io.gfile.GFile(spm_path, mode="rb") as f:
        sp.LoadFromSerializedProto(f.read())
    print("SentencePiece model loaded at {}.".format(spm_path))

    messages = []
    messages.append(userInput)

    values, indices, dense_shape = process_to_IDs_in_sparse_format(sp, messages)

    # Reduce logging output.
    logging.set_verbosity(logging.ERROR)

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(
            encodings,
            feed_dict={input_placeholder.values: values,
                       input_placeholder.indices: indices,
                       input_placeholder.dense_shape: dense_shape})

        print(message_embeddings[0])
        return message_embeddings[0]
        #for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
        #    print("Message: {}".format(messages[i]))
        #   print("Embedding size: {}".format(len(message_embedding)))
        #    message_embedding_snippet = ", ".join(
        #        (str(x) for x in message_embedding[:3]))
        #    print("Embedding: [{}, ...]\n".format(message_embedding_snippet))

def process_to_IDs_in_sparse_format(sp, sentences):
  # An utility method that processes sentences with the sentence piece processor
  # 'sp' and returns the results in tf.SparseTensor-similar format:
  # (values, indices, dense_shape)
  ids = [sp.EncodeAsIds(x) for x in sentences]
  max_len = max(len(x) for x in ids)
  dense_shape=(len(ids), max_len)
  values=[item for sublist in ids for item in sublist]
  indices=[[row,col] for row in range(len(ids)) for col in range(len(ids[row]))]
  return (values, indices, dense_shape)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        # get form data
        data = []
        user_description = request.form['userInput']
        user_description_embedding = create_embeddings(user_description)
        labels, distances = p.knn_query(user_description_embedding, k = 5)
        labels_to_return = labels[0]
        recommendations_user_text = []
        for index in labels_to_return:
            recommendations_user_text.append(index)
        #print(labels_to_return)
        print(recommendations_user_text)
        return render_template('index.html', recommendations_user_text=recommendations_user_text)

if __name__ == '__main__':

    p = hnswlib.Index(space='cosine', dim=512)
    p.load_index("./notebooks/index.bin")


    print(class_data[0])
    def embed(input):
        return model(input)
    app.run(debug=True)

