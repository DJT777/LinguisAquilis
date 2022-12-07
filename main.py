from flask import Flask, render_template, request, jsonify, redirect, url_for
from absl import logging
import tensorflow as tf
import tensorflow_hub as hub
import os
import re
import hnswlib
import json
import laUSEv5 as aq
from database import database
from visitor import Visitor
from form import Form
#from flask_ngrok import run_with_ngrok

app = Flask(__name__)
#run_with_ngrok(app)
class_json = open('data.json')
class_data = json.load(class_json)



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
                code, classification = p1.classify(majorDescription)
                return_recommendation = [code + " - " + classification]
                # print("Recommendation: ",return_recommendation);
                myDb.insertMajor('describeMajor', classification)
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
    app.run()
