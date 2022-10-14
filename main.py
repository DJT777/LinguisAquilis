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

app = Flask(__name__)
class_json = open('data.json')
class_data = json.load(class_json)

def create_embeddings(userInput):
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
    #print("SentencePiece model loaded at {}.".format(spm_path))

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

        #print(message_embeddings[0])
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

def filter_course(course):
    if(course not in class_data):
        return True
    else:
        return False

@app.route("/findcourses", methods=['GET', 'POST', "PUT"])
def findcourses():
    dropdown_list = []
    for x in class_data:
            if x['course_title'] not in dropdown_list:
                    dropdown_list.append(x['course_dept'].strip() + " " + x['course_number'].strip() +" " + x['course_title'].strip())
    if request.method == "GET":
        #filteredData = filter(filter_course, class_data_copy)
        return render_template('findcourses.html', mymethod="GET",dropdownList=dropdown_list,
                            recommendedClasses =dropdown_list, containsData="False")
    if request.method == "POST":
            if request.form['submitButton'] == "Submit User Description":
                user_description = request.form['userInputDescription']
                print("User Description: " + user_description)
                user_description_embedding = create_embeddings(user_description)
                p = hnswlib.Index(space='cosine', dim=512)
                p.load_index("./notebooks/index.bin")
                labels, distances = p.knn_query(user_description_embedding, k=5)
                labels_to_return = labels[0]
                recommendations_user_text = []
                for index in labels_to_return:
                    recommendations_user_text.append(class_data[index])
                    print(class_data[index]['course_title'])
                # print(labels_to_return)
                # print(recommendations_user_text)
                return render_template('findcourses.html',dropdownList=dropdown_list,
                                        recommendedClasses=recommendations_user_text, containsData="True", containsDataMajor="False")
            if request.form['submitButton'] == "Find Similar":
                print("SELECTED CLASS:" + request.form['selectClass'])
                selectedClass = request.form['selectClass']
                selectedClassEmbedding = create_embeddings(selectedClass)
                p = hnswlib.Index(space='cosine', dim=512)
                p.load_index("./notebooks/index.bin")
                labels, distances = p.knn_query(selectedClassEmbedding, k=5)
                labels_to_return = labels[0]
                recommendations_user_text = []
                for index in labels_to_return:
                    recommendations_user_text.append(class_data[index])
                    print(class_data[index])
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                        recommendedClasses = recommendations_user_text, containsData="True", containsDataMajor="False")
            if request.form['submitButton'] == "Find a Major":
                print("MAJOR INTERESTS:" + request.form['userInputMajor'])
                majorDescription = request.form['userInputMajor']
                selectedMajorEmbedding = create_embeddings(majorDescription)
                p = hnswlib.Index(space='cosine', dim=512)
                p.load_index("./notebooks/index.bin")
                labels, distances = p.knn_query(selectedMajorEmbedding, k=5)
                labels_to_return = labels[0]
                recommendations_user_text = []
                recommended_majors = []
                for index in labels_to_return:
                    recommendations_user_text.append(class_data[index])
                    if class_data[index]['course_dept'] not in recommended_majors:
                        recommended_majors.append(class_data[index]['course_dept'])
                    print(class_data[index])
                print(recommended_majors)
                recommended_major = max(recommended_majors)
                return_recommendation = []
                return_recommendation.append(recommended_major)
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                        recommendedClasses = recommended_majors, containsData="False", containsDataMajor="True")

@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == "GET":
        index_course_list = open('data\quick-rec.json')
        index_course_list = json.load(index_course_list)
        return render_template('index.html', quickRec = index_course_list)
    if request.method == "POST":
        if request.form["submitButton"] == "Find Courses":
            return redirect(url_for("findcourses")) 
        print("Request.Form: ")
        # output = request.form.getlist('name[]')
        output = request.form.to_dict(flat=False)
        for item in output:
            output = item
        # print(output.items())
        # return '<h1>Hello Default</h1>
        quickEmbbedings = create_embeddings(output)
        p = hnswlib.Index(space='cosine', dim=512)
        p.load_index("./notebooks/index.bin")
        labels, distances = p.knn_query(quickEmbbedings, k=5)
        labels_to_return = labels[0]
        recommendations_user_text = []
        for index in labels_to_return:
            recommendations_user_text.append(class_data[index])
        return render_template("results.html", returnList = recommendations_user_text)
    else:
        # get form data
        return '<h1>Hello Default</h1>'

if __name__ == '__main__':

    p = hnswlib.Index(space='cosine', dim=512)
    p.load_index("./notebooks/index.bin")
   # print(class_data[0])

    app.run(debug=True)

def embed(input):
    return model(input)