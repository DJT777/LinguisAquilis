import this
import requests

from database import database

class Visitor:
    city = ''
    region = ''
    country = ''
    zip = ''
    timezone = ''
    data = None
    database = None

    def __init__(self, database) -> None:
        self.data = self.getData()
        self.database = database
        self.database.path = './data/sql.db'
        # self.printData()
        pass

    def printData(self):
        print(f'City: {self.data["city"]}')
        print(f'Region: {self.data["region"]}')
        print(f'Country: {self.data["country"]}')
        print(f'ZIP: {self.data["postal"]}')
        print(f'Timezone: {self.data["timezone"]}')

    def getData(self):
        try:
            data = requests.get('https://ipinfo.io/json')
            data = data.json()
            # print(f'You are located in {data["city"]}')
            return data
        except:
            print('Error Getting Visitor Data')
            return False    
    def logVisitor(self):
        try:
            self.database.createVisitorTable('visitors')
            self.database.insertVisitor(self.data,'visitors')
            self.database.getVisitorInfo('visitors')
        except:
            print('Error Logging Visitor Data')  