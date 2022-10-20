from flask import Flask, render_template, request, jsonify, redirect, url_for
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
import sentencepiece



class useLite:
    name = "Hello World"


    def filter_course(course):
        if (course not in class_data):
            return True
        else:
            return False

    def process_to_IDs_in_sparse_format(self, sp, sentences):
        # An utility method that processes sentences with the sentence piece processor
        # 'sp' and returns the results in tf.SparseTensor-similar format:
        # (values, indices, dense_shape)
        ids = [sp.EncodeAsIds(x) for x in sentences]
        max_len = max(len(x) for x in ids)
        dense_shape = (len(ids), max_len)
        values = [item for sublist in ids for item in sublist]
        indices = [[row, col] for row in range(len(ids)) for col in range(len(ids[row]))]
        return (values, indices, dense_shape)

    def create_embeddings(self, userInput):
        module = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-lite/2")
        # module = hub.Module("module\universal-sentence-encoder-lite_2\tfhub_module.pb")
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
        # print("SentencePiece model loaded at {}.".format(spm_path))

        messages = []
        messages.append(userInput)

        values, indices, dense_shape = self.process_to_IDs_in_sparse_format(sp, messages)

        # Reduce logging output.
        logging.set_verbosity(logging.ERROR)

        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            message_embeddings = session.run(
                encodings,
                feed_dict={input_placeholder.values: values,
                           input_placeholder.indices: indices,
                           input_placeholder.dense_shape: dense_shape})

            # print(message_embeddings[0])
            return message_embeddings[0]
            # for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
            #    print("Message: {}".format(messages[i]))
            #   print("Embedding size: {}".format(len(message_embedding)))
            #    message_embedding_snippet = ", ".join(
            #        (str(x) for x in message_embedding[:3]))
            #    print("Embedding: [{}, ...]\n".format(message_embedding_snippet))

    def __init__(self):
        self.class_json = open('data.json')
        self.class_data = json.load(self.class_json)
        self.name = "Muhammad"
        print(self.name)


p1 = useLite()
embedding = p1.create_embeddings("AFRC 311 Africana Studies Perspectives")
print(p1.name)
print(embedding)
print("Alhamdullilah")