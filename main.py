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
from visitor import Visitor
from form import Form

app = Flask(__name__)
class_json = open('data.json')
class_data = json.load(class_json)
major_dict = {"ACCT": "Accounting", "ADV":"Advertising", "AFRC":"Africana Studies", "AGBU":"Agricultural Business", "AHA":"Arts and Heritage Administration", "ANTH":"Anthropology", "ARAB":"Arabic Studies", "ART":"Art",
              "ARTD":"Art & Design", "ARTE":"Art Education", "ARTH":"Art History", "ARTP":"Photography", "ASTR":"Astronomy", "BAN":"Business Analytics", "BCOM":"Business Communication", "BIOL":"Biology",
              "BLAW":"Business Law", "BUAD":"Business Administration", "CE":"Civil Engineering", "CHEM":"Chemistry", "CHIN":"Chinese", "CIS":"Computer Information Systems", "CMST":"Communication Studies", "COMM":"Communications",
              "CRIM": "Criminology", "CS":"Computer Science", "DMS":"Diagnostic Medical Sonography", "DSCI":"Data Science", "DTAS":"Dental Assisting", "DTHY":"Dental Hygiene", "DVT":"Diagnostic Vascular Sonography", "ECE":"Electrical Engineering",
              "ECHO":"Echocardiography", "ECON": "Economics", "EDUC": "Education", "ENG":"English", "ENGR":"Engineering", "EXSC":"Exercise Science", "FIN":"Finance", "FREN":"French", "GENS":"Generla Studies", "GEOG":"Geography",
              "GEOL":"Geology", "GERM":"German", "GERO":"Gerontology", "GLST":"Global Studies", "GNDR":"Gender Studies", "HA":"Health Administration", "HI":"Health Informatics and Information Management", "HIST":"History",
              "HONS":"Honors", "HP":"Health Professions", "HUM":"Humanities", "IEP":"Intensive English Program", "IME":"Industrial and Manufacturing Engineering", "IPH":"Interprofessional Health", "JPN":"Japanese",
              "JRN":"Journalism", "KIN":"Kinesiology", "LATN":"Latin", "LIBA":"Liberal Arts", "MATH":"Mathematics", "ME":"Mechanical Engineering", "MFET":"Manufacting Engineering Technology", "MKTG":"Marketing", "MNGT":"Management",
              "MS":"Military Science", "MUS":"Music", "NURS":"Nursing", "NUTR":"Nutrition", "OTA":"Occupational Therapy Assistant", "PET":"Physical Education Teaching", "PH":"Public Health", "PHIL":"Philosophy", "PHYS":"Physics", "POLS":"Political Science",
              "PRFS":"Professional Studies", "PRL":"Public Relations", "PSY":"Psychology", "RADT":"Radiologic Technology", "RELS":"Religious Studies", "REST":"Respiratory Therapy", "RTV":"Radio and Television", "SOC":"Sociology",
              "SOCW":"Social Work", "SPAN":"Spanish", "SPTM":"Sports Management", "STAT":"Statistics", "STEM":"Science, Technology, Engineering, & Mathematics", "TECH":"Technology", "THTR":"Theatre", "UNIV":"University Studies",
              "WLC":"World Languages and Cultures"}


@app.route("/findcourses", methods=['GET', 'POST', "PUT"])
def findcourses():
    dropdown_list = []
    for x in class_data:
            if x['course_title'] not in dropdown_list:
                    dropdown_list.append(x['course_dept'].strip() + " " + x['course_number'].strip() +" " + x['course_title'].strip())
    if request.method == "GET":
        return render_template('findcourses.html', mymethod="GET",dropdownList=dropdown_list,
                            recommendedClasses =dropdown_list, containsData="False")
    if request.method == "POST":
            if request.form['submitButton'] == "Submit User Description":
                user_description = request.form['userInputDescription']
                print("User Description: " + user_description)
                user_description_embedding = p1.create_embeddings(user_description)
                recommendation = p1.query_embedding(user_description_embedding, user_description)
                myDb.insertClass(recommendation.recommendations_user_text, 'describeClass')
                myDb.insertClass(recommendation.recommendations_user_text, 'classlist')
                return render_template('findcourses.html',dropdownList=dropdown_list,
                                        recommendedClasses=recommendation.recommendations_user_text, containsData="True", 
                                        containsDataMajor="False", userQuery = user_description)
            if request.form['submitButton'] == "Find Similar":
                print("SELECTED CLASS:" + request.form['selectClass'])
                selectedClass = request.form['selectClass']
                selectedClassEmbedding = p1.create_embeddings(selectedClass)
                recommendation = p1.query_embedding(selectedClassEmbedding, selectedClass)
                myDb.insertClass(recommendation.recommendations_user_text, 'selectClass')
                myDb.insertClass(recommendation.recommendations_user_text, 'classlist')
                for recommended_class in recommendation.recommendations_user_text:
                    myDb.courseExists(recommended_class, 'selectClass')
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                        recommendedClasses = recommendation.recommendations_user_text, containsData="True", 
                                        containsDataMajor="False",userQuery = selectedClass)
            if request.form['submitButton'] == "Find a Major":
                print("MAJOR INTERESTS:" + request.form['userInputMajor'])
                majorDescription = request.form['userInputMajor']
                selectedMajorEmbedding = p1.create_embeddings(majorDescription)
                recommendation = p1.query_embedding(selectedMajorEmbedding, majorDescription)
                return_recommendation = []

                return_recommendation.append(recommendation.recommended_major + " - " + major_dict[recommendation.recommended_major])
                # print("Recommendation: ",return_recommendation);
                myDb.insertMajor('describeMajor', major_dict[recommendation.recommended_major])
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                        recommendedClasses =return_recommendation, containsData="False", containsDataMajor="True",
                                        userQuery = majorDescription)
            if request.form['submitButton'] == "Submit Feedback":
                option = request.form['option']
                print(p1.currentRecommendation.recommendations_user_text)
                myDb.insertFeedback(p1.currentRecommendation.recommendations_user_text, 'userFeedback', option)
                return render_template('findcourses.html', mymethod="GET", dropdownList=dropdown_list,
                                       recommendedClasses=dropdown_list, containsData="False")
    else:
        return render_template("error.html")

@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == "GET":
        index_course_list = open('data/quick-rec.json')
        index_course_list = json.load(index_course_list)
        return render_template('index.html', quickRec = index_course_list)
    if request.method == "POST":
        queryDescription = request.form['query']
        embeddings = p1.create_embeddings(queryDescription);
        recommendations = p1.query_embedding(embeddings, queryDescription);
        myDb.insertClass(recommendations.recommendations_user_text, "quickrecs");
        return render_template("results.html", returnList = recommendations.recommendations_user_text, userQuery=queryDescription)
    else:
        return render_template("error.html")

@app.route("/insights", methods=['GET'])
def insights():
    insightsData = visitor.getInsightData()
    return render_template("insights.html", insight=insightsData)

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/error", methods=['GET'])
def error():
    return render_template("error.html")

@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    if request.method == "POST":
        form.name = request.form['name']
        form.email = request.form['email']
        form.phoneNumber = request.form['phone']
        form.contactChoice = request.form['contact_choice']
        form.notes = request.form['notes']
        form.logForm()
        return render_template("contact.html")

@app.route("/contactportal", methods=['GET','POST'])
def contactportal():
    if request.method == "GET":
        formList = myDb.executeDataQuery("contact")
        return render_template("contactportal.html", list=formList)
    if request.method == "POST":
        formId = request.form.get("id")
        myDb.markFromComplete(formId);
        formList = myDb.executeDataQuery("contact")
        return render_template("contactportal.html", list=formList)

if __name__ == '__main__':
    p1 = aq.useLite()
    myDb = database()
    myDb.initDatabase()
    visitor = Visitor(myDb)
    visitor.logVisitor()
    form = Form(myDb)
    app.run(debug=True)
