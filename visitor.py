import requests
from database import database

class Visitor:
    data = None
    database = None
    insightData = None

    #Constructor automatically gets user data
    def __init__(self, database) -> None:
        self.data = self.getData()
        self.database = database
        self.database.path = './data/sql.db'
        pass

    #Prints data
    def printData(self):
        print(f'City: {self.data["city"]}')
        print(f'Region: {self.data["region"]}')
        print(f'Country: {self.data["country"]}')
        print(f'ZIP: {self.data["postal"]}')
        print(f'Timezone: {self.data["timezone"]}')

    def getData(self):
        try:
            #This endpoint returns the data
            data = requests.get('https://ipinfo.io/json')
            #Format data as JSON
            data = data.json()
            return data
        except Exception as e:
            print('Error Getting Visitor Data - ', e)
            return False    
    
    def logVisitor(self):
        try:
            self.database.insertVisitor(self.data,'visitors')
        except Exception as e:
            print('Error Logging Visitor Data: ', e)  
    
    def getInsightData(self):
        try:
            self.insightData = self.database.getVisitorCityInfo('Visitors')
            self.insightData['topCourse'] = self.database.getTopCourses('Classlist')
            self.insightData['topMajor'] = self.database.getTopMajor('describeMajor')
        except Exception as e:
            print("Error Getting Data InsightData: ", e)
        finally:
            return self.insightData