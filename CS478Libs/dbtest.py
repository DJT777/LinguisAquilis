from database import database
from visitor import Visitor
from form import Form

mylist = [
    {
        "course_dept": "ACCT",
        "course_number": "201",
        "course_title": "Accounting Principles I"
    },
    {
        "course_dept": "IME",
        "course_number": "331",
        "course_title": "Introduction to Statistical Quality Control"   
    },
    {
        "course_dept": "REST",
        "course_number": "325",
        "course_title": "Advanced Pulmonary Diseases"
    }
]
sampleCourse =     {
    "course_dept": "REST",
    "course_number": "325",
    "course_title": "Advanced Pulmonary Diseases"
}

myDb = database()
myDb.initDatabase()
myDb.path = './data/sql.db'
# myDb.testCursor()
# myDb.dropTable('classlist')
# myDb.createTable('classlist')
# myDb.insertClass(mylist, 'classlist')
# myDb.insertSingleClass(mylist[0], 'classlist')
# # myDb.closeConnection()
# myDb.courseExists(sampleCourse, 'classlist')
# myDb.getAllTableData("feedback")


# # myDb.courseExists(sampleCourse, 'classlist')
# # myDb.courseExists(sampleCourse, 'classlist')
# myDb.getTopCourses('classlist')

# visitor = Visitor(myDb)
# visitor.getData()
# visitor.printData()
form = Form(myDb)
# form.name = "Patrick Warburton"
# form.email = "user5@gmail.com"
# form.phoneNumber ="720 445 2341"
# form.notes = "I would like more information about this"
# form.contactChoice = "Email"
# form.logForm()
form.name = "Marcos Smith"
form.email = "user2@gmail.com"
form.phoneNumber ="812 322 3221"
form.notes = "This helped so much!"
form.contactChoice = "Email"
form.logForm()
form.name = "Petter Griffin"
form.email = "user3@gmail.com"
form.phoneNumber ="812 322 3221"
form.notes = "How did you guys do this?"
form.contactChoice = "Phone"
form.logForm()
form.name = "Austin Powers"
form.email = "user4@gmail.com"
form.phoneNumber ="812 322 3221"
form.notes = "This is what I have been waiting for!"
form.contactChoice = "Email"
form.logForm()
# myDb.markFromComplete("475");
#myDb.insertForm(form)
# myDb.getVisitorCityInfo('Visitors')
# myDb.getTopCourses('Classlist')
# myDb.getTopCourses('Classlist')
# myDb.dropTable("contact")
# myDb.createFormTable("contact")
# myDb.getAllTableData("contact")

#Feedback
# myDb.dropTable("feedback");
# myDb.createFeedbackTable("feedback")
# myDb.insertFeedback(mylist,"feedback", 0)
# myDb.getAllTableData("feedback")

        