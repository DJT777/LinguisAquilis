from flask import Flask, render_template, request
from NLPlibs import BERT
from NLPlibs import USE
#from NLPlibs import ELMO
from NLPlibs import glove
from NLPlibs import llama
from NLPlibs import OpenAi
from NLPlibs import word2vec
from NLPlibs import bagofwords
from NLPlibs import TFIDF
import json
#from flask_ngrok import run_with_ngrok


app = Flask(__name__)
#run_with_ngrok(app)
class_json = open('notebooks/USE-BERT-BOW-Word2Vec-TFIDF-GLOVE-OpenAI-ELMO-cleaned.json')
class_data = json.load(class_json)
model = None



@app.route("/findcourses", methods=['GET', 'POST', "PUT"])
def findcourses():
    global model
    dropdown_list = []
    for x in class_data:
            if x['course_title'] not in dropdown_list:
                    dropdown_list.append(x['course_dept'].strip() + " " + x['course_number'].strip() +" " + x['course_title'].strip())
    if request.method == "GET":
        return render_template('findcourses.html', mymethod="GET",dropdownList=dropdown_list,
                            recommendedClasses =dropdown_list, containsData="False")


    if request.method == "POST":
            if request.form['submitButton'] == "Find Similar":
                print("SELECTED CLASS:" + request.form['selectClass'])
                selectedClassIndex = dropdown_list.index(request.form['selectClass'])
                selectedClass = request.form['selectClass']
                selectedClassEmbedding = class_data[selectedClassIndex][model.type + '_embedding']
                sortedResults = model.compare(selectedClassEmbedding, class_data)
                print(sortedResults)
                recommendations = []
                for i, (index, similarity) in enumerate(sortedResults[:5]):
                    recommendations.append(class_data[index])
                return render_template("findcourses.html", dropdownList=dropdown_list, recommendedClasses = recommendations, containsData="True", containsDataMajor="False",userQuery = selectedClass)

            if request.form['submitButton'] == "Submit User Description":
                userDescription = request.form['userInputDescription']
                print("USER SEARCH:" + request.form['userInputDescription'])
                selectedClassEmbedding = model.embed([userDescription])
                if model.type == "OpenAI":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                elif model.type == "glove":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                elif model.type == "word2vec":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                elif model.type == "TFIDF":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                elif model.type == "BagOfWords":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                elif model.type == "ELMO":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                elif model.type == "BERT":
                    sortedResults = model.compare(selectedClassEmbedding, class_data)
                else:
                    sortedResults = model.compare(selectedClassEmbedding[0], class_data)
                print(sortedResults)
                recommendations = []
                for i, (index, similarity) in enumerate(sortedResults[:5]):
                    recommendations.append(class_data[index])
                return render_template("findcourses.html", dropdownList=dropdown_list,
                                       recommendedClasses=recommendations, containsData="True",
                                       containsDataMajor="False", userQuery=userDescription)
    else:
        return render_template("error.html")



@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    global model
    if request.method == "GET":
        index_course_list = open('data/txt/quick-rec.json')
        index_course_list = json.load(index_course_list)

        return render_template('index.html', quickRec = index_course_list)
    if request.method == "POST":
        selected_model = request.form['model']  # Get the selected model from the form

        # Process the selected model and perform your desired actions
        # For example, you can load the selected model into memory
        if selected_model == 'LLaMa':
            model = llama.Llama7bEmbedding()
            print("Loaded LLaMa")
            pass
        if selected_model == 'USE':
            model = USE.USE('https://tfhub.dev/google/universal-sentence-encoder-large/5')
            print("Loaded USE")
            pass
        elif selected_model == 'BERT':
            model = BERT.BERT('bert-base-uncased')
            print("Loaded BERT")
            pass
        elif selected_model == 'OpenAI':
            model = OpenAi.OpenAI("")
            print("Loaded OpenAI")
            pass
        elif selected_model == 'ELMO':
            model = ELMO.ELMo("https://tfhub.dev/google/elmo/3")
            print("Loaded ELMO")
            pass
        elif selected_model == 'GloVe':
            model = glove.GloVe()
            print("Loaded GloVe")
            pass
        elif selected_model == 'Word2Vec':
            model = word2vec.Word2VecModel()
            print("Loaded Word2Vec")
            pass
        elif selected_model == 'TF-IDF':
            model = TFIDF.TFIDF()
            print("Loaded TF-IDF")
            pass
        elif selected_model == 'Bag of Words':
            model = bagofwords.BagOfWords()
            print("Loaded Bag of Words")
            pass
        # Add more cases for other models
        return render_template("index.html")

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
    #p1 = aq.useLite()
    app.run()
