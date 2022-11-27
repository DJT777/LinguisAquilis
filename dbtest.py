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
myDb.path = './data/sql.db'
myDb.testCursor()
myDb.dropTable('classlist')
myDb.createTable('classlist')
myDb.insertClass(mylist, 'classlist')
# # myDb.closeConnection()
# myDb.courseExists(sampleCourse, 'classlist')
myDb.getAllTableData("classlist")


# # myDb.courseExists(sampleCourse, 'classlist')
# # myDb.courseExists(sampleCourse, 'classlist')
# myDb.getTopCourses('classlist')

# visitor = Visitor(myDb)
# form = Form(myDb)
# form.name = "Catalina Virgina"
# form.email = "user@gmail.com"
# form.phoneNumber ="812 322 3221"
# form.notes = "I need this on my campus!"
# form.contactChoice = "Email"
# form.logForm()
# myDb.markFromComplete("475");
#myDb.insertForm(form)
# myDb.getVisitorCityInfo('Visitors')
# myDb.getTopCourses('Classlist')
# myDb.getTopCourses('Classlist')
# myDb.dropTable("contact")
# myDb.createFormTable("contact")
# myDb.getAllTableData("contact")



        