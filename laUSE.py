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


#Path to create recommendation class halted because inner classes cannot inherit outer classes
#thus making it impossible to inherit the create embedding method/function from the outer class
class Recommendation:
    def __init__(self):
        self.query = None
        self.queryLabels = None
        self.registrarData = None
        self.helloWorld = "Hello World"
        print(self.helloWorld)


    #Constructor Pass in a query and the labels returned by useLite's create_embedding() and query_embedding() functions
    def __init__(self, userQueryString, userQueryEmbedding, userQueryLabels, userQueryDistances):
        self.user = None
        self.class_json = open('data.json')
        self.class_data = json.load(self.class_json)
        self.p = hnswlib.Index(space='cosine', dim=512)
        self.p.load_index("./notebooks/index.bin")
        self.userQueryString = userQueryString
        self.userQueryEmbedding = userQueryEmbedding
        self.userQueryLabels = userQueryLabels
        self.queryDistances = userQueryDistances
        self.recommendations_user_text = []
        labels_to_return = userQueryLabels[0]
        print("Your results for your search of " + self.userQueryString + " returned these results...")
        for index in labels_to_return:
            self.recommendations_user_text.append(self.class_data[index])
            print(self.class_data[index]['course_title'])

        #self.helloWorld = "Hello World"
        #print(self.helloWorld)



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

    def query_embedding(self, user_description_embedding, user_description_string):
        labels, distances = self.p.knn_query(user_description_embedding, k=5)
        #print(labels)
        recommendation = Recommendation(user_description_string, user_description_embedding, labels, distances)
        print(recommendation.userQueryString)

        return recommendation


    def __init__(self):
        self.name = "Muhammad"
        self.class_json = open('data.json')
        self.class_data = json.load(self.class_json)
        self.p = hnswlib.Index(space='cosine', dim=512)
        self.p.load_index("./notebooks/index.bin")
        #print(self.name)
        #print("A sample embedding")
        #print(self.sampleEmbedding)



