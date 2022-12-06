from datetime import datetime
import random
class Form:
    id = None
    name = None
    email = None
    contactChoice = None
    phoneNumber = None
    notes = None
    timeStamp = None
    completed = 0
    database = None

    def __init__(self, database):
        now = datetime.now()
        self.timeStamp = now.date()
        self.database = database
    
    def logForm(self):
        try:
            self.id = random.randint(100, 999)
            self.database.insertForm(self)
        except Exception as e:
            print("Error at Inserting Form: ", e)
    def getAllForms(self):
        try:
            self.database.getAllTableData("contact")
        except Exception as e:
            print("Error at Getting Forms: ", e)
            