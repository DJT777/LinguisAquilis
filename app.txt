from flask import Flask, render_template, request, redirect,url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        return redirect(url_for("findcourses"))   
    else:
        # get form data
        return '<h1>Hello Default</h1>'

@app.route("/findcourses", methods=['GET', 'POST'])
def findcourses():
    classes = ['Class 1','Class 2','Class 3']
    if request.method == "GET":
        return render_template('findcourses.html', mymethod="GET")
    if request.method == "POST":
        return render_template('results.html', mymethod="POST", returnList=classes)  
    else:
        # get form data
        return '<h1>Hello Default</h1>'
if __name__ == '__main__':
    app.run(debug=True)