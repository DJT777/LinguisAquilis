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
import laUSE as aq
from  database import  database

app = Flask(__name__)
class_json = open('data.json')
class_data = json.load(class_json)



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
                user_description_embedding = p1.create_embeddings(user_description)
                recommendation = p1.query_embedding(user_description_embedding, user_description)
                myDb.insertClass(recommendation.recommendations_user_text, 'describeClass')
                # for recommended_class in recommendation.recommendations_user_text:
                #    myDb.courseExists(recommended_class, 'classlist')
                return render_template('findcourses.html',dropdownList=dropdown_list,
                                        recommendedClasses=recommendation.recommendations_user_text, containsData="True", containsDataMajor="False")
            if request.form['submitButton'] == "Find Similar":
                print("SELECTED CLASS:" + request.form['selectClass'])
                selectedClass = request.form['selectClass']
                selectedClassEmbedding = p1.create_embeddings(selectedClass)
                recommendation = p1.query_embedding(selectedClassEmbedding, selectedClass)
                myDb.insertClass(recommendation.recommendations_user_text, 'selectClass')
                for recommended_class in recommendation.recommendations_user_text:
                    myDb.courseExists(recommended_class, 'selectClass')
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                        recommendedClasses = recommendation.recommendations_user_text, containsData="True", containsDataMajor="False")
            if request.form['submitButton'] == "Find a Major":
                print("MAJOR INTERESTS:" + request.form['userInputMajor'])
                majorDescription = request.form['userInputMajor']
                selectedMajorEmbedding = p1.create_embeddings(majorDescription)
                recommendation = p1.query_embedding(selectedMajorEmbedding, majorDescription)
                myDb.insertClass(recommendation.recommendations_user_text, 'describeMajor')
                # for recommended_class in recommendation.recommendations_user_text:
                #    myDb.courseExists(recommended_class, 'classlist')
                return_recommendation = []
                return_recommendation.append(recommendation.recommended_major)
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                        recommendedClasses =return_recommendation, containsData="False", containsDataMajor="True")
            if request.form['submitButton'] == "Submit Feedback":
                option = request.form['option']
                #TODO: INCLUDE THE BOOLEAN VARIABLE FOR HELPFULNESS OF RECOMMENDATION
                myDb.insertClass(p1.currentRecommendation.recommendations_user_text, 'userFeedback')
                return render_template('findcourses.html', mymethod="GET", dropdownList=dropdown_list,
                                       recommendedClasses=dropdown_list, containsData="False")

@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == "GET":
        index_course_list = open('data/quick-rec.json')
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
        quickEmbbedings = p1.create_embeddings(output)
        recommendation = p1.query_embedding(quickEmbbedings, output)
        return render_template("results.html", returnList = recommendation.recommendations_user_text)
    else:
        # get form data
        return '<h1>Hello Default</h1>'

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/contact", methods=['GET'])
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    p1 = aq.useLite()
    testQuery = "this is a test"
    myDb = database()
    myDb.path = './data/sql.db'
    myDb.createTable('selectClass')
    myDb.createTable('describeClass')
    myDb.createTable('describeMajor')
    myDb.createTable('userFeedback')

    app.run(debug=True)

def embed(input):
    return model(input)