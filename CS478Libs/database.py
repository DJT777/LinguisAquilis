import random
import threading
import sqlite3
from course import Course
from math import floor

class database:
    path = ""
    mycursor = None
    sqlConnection = None
    lock = None
    #Class Constructor
    def __init__(self):
        try:
            self.sqlConnection = sqlite3.connect(self.path, check_same_thread=False)
            cursor = self.sqlConnection.cursor()
            self.mycursor = cursor
            self.lock = threading.Lock()
        except sqlite3.Error as error:
            print('Error occured Init - ', error)
    #Initializing the database
    def initDatabase(self):
        try:
            self.path = './data/sql.db'
            self.createTable('selectClass')
            self.createTable('describeClass')
            self.createMajorTable('describeMajor')
            self.createTable('userFeedback')
            self.createTable('classlist')
            self.createVisitorTable("visitors")
            self.createFormTable('contact')
        except Exception as e:
            print("Error initializing database - ", e)

    def testCursor(self):
        if self.sqlConnection:
            try:
                self.mycursor.execute("select sqlite_version();")
                result = self.mycursor.fetchall()
                print('SQLite Version is: {}'.format(result))
            except sqlite3.Error as error:
                print('Error occured at Testing Database - ', error)
            finally:
                self.closeConnection()  
        else:
            self.connectDatabase()
            self.testCursor()

    def connectDatabase(self):
        try:
            self.sqlConnection = sqlite3.connect(self.path,  check_same_thread=False)
            cursor = self.sqlConnection.cursor()
            self.mycursor = cursor
            print('SQL Connection Open')
        except sqlite3.Error as error:
            print('Error occured at Connecting Database - ', error)    

    def closeConnection(self):
        if self.sqlConnection:
            self.sqlConnection.close()
            print('SQL connection closed.')
    
    def dropTable(self, table):
        if self.sqlConnection:
            try:
                self.lock.acquire(True)
                self.connectDatabase()
                self.mycursor.execute("DROP TABLE IF EXISTS " +table)
                print("Dropped: " +table)
            except sqlite3.Error as error:
                print('Error occured at DropTable - ', error)  
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            self.connectDatabase()
            self.dropTable()

    def getAllTableData(self, table):
        if self.sqlConnection:
            try:
                self.lock.acquire(True)
                self.connectDatabase()
                query = "SELECT * FROM " +table
                self.mycursor.execute(query)
                data = self.mycursor.fetchall()
                if len(data) < 1:
                    print(table+' table is empty')
                    return False;
                else:
                    print('All data in table', table, '\n')
                    for row in data:
                        print(row)
                print('Table size is: ', len(data))
                self.sqlConnection.commit()
                return data
            except sqlite3.Error as error:
                print('Error Getting Table ', table)
                print('Error occured  - ', error)  
                return False;
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            self.connectDatabase()
            self.getAllTableData()
#Course Section
    def createTable(self, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                query = "CREATE TABLE IF NOT EXISTS " +table+ " (id INT, dept TEXT, title TEXT, number TEXT, score INT);"
                self.mycursor.execute(query)
                print('CreatedTable: ', table)
            except sqlite3.Error as error:
                print('Error occured at Creating Table ' + table+' - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.createTable()

    def insertSingleClass(self, course, table):
        count = 0
        if self.sqlConnection:
            try:
                self.connectDatabase()
                courseId = course['course_dept'] + course['course_number']
                courseId.strip(courseId)
                self.mycursor.execute("INSERT or IGNORE INTO " + table + " VALUES(?, ?, ?, ?, ?);", (courseId, course['course_dept'], course['course_title'], course['course_number'], 1))
                count += self.mycursor.rowcount
                self.sqlConnection.commit()
                print('Inserted: ',count, ' rows at '+ table +',')    
            except sqlite3.Error as error:
                print('Error occured at InsertSingleClass - ', error)  
                print('Failed to insert: - ', courseId)  
            finally:
                self.closeConnection()
        else:
            self.connectDatabase()
            self.insertSingleClass()
 
    def increment(self, courseId, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.mycursor.execute("UPDATE " + table +" SET score = score + 1 WHERE id = ? ",(courseId,))
                self.sqlConnection.commit()
                print('Commited')
            except sqlite3.Error as error:
                print('Error occured at Increment - ', error) 
            finally:
                self.closeConnection()
        else:
            print('Cannot increment')
    
    def insertClass(self, courses, table):
        if self.sqlConnection:
            try:
                self.lock.acquire(True)
                self.connectDatabase()
                for course in courses:
                    self.courseExists(course, table)
            except sqlite3.Error as error:
                print('Error occured at insertClass - ', error)  
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            self.connectDatabase()
            self.insertClass()

    def courseExists(self, course, table):
        try:
            self.connectDatabase()
            courseId = course['course_dept'] + course['course_number'] 
            self.mycursor.execute("SELECT * FROM "+ table +" WHERE id = ?", (courseId,))
            count = self.mycursor.fetchone() is not None
            print('Id: ',courseId , ' is ' , count)
            if count:
                self.increment(courseId, table)
            else:
                print('Add Course ', courseId, ' does not exist. Adding now.')
                self.insertSingleClass(course, 'classlist')
        except sqlite3.Error as error:
                print('Error occured at exists - ', error)  
        finally:
            self.closeConnection()

    def getTopCourses(self, table):
        try:
            courseList = []
            self.lock.acquire(True)
            self.connectDatabase()
            self.mycursor.execute('''SELECT score, dept, number, title FROM classlist ORDER BY score DESC LIMIT 5''')
            data = self.mycursor.fetchall()
            if(len(data) > 0):
                print('All data in table', table, '\n')
                for row in data:
                    course = Course()
                    course.name = row[1]
                    course.code = row[2]
                    course.description = row[3]
                    courseList.append(course)
                    course = None
            else:
                print('Table size is ', len(data))    
        except sqlite3.Error as error:
            print('Error occured at Top Courses - ', error)      
        finally:
            self.lock.release()
            self.closeConnection()
            return courseList   
    
    def insertMajor(self, table, major):
        count = 0
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                self.mycursor.execute("INSERT INTO "+ table+" (name) VALUES('"+major+"')")
                self.sqlConnection.commit()
                count = self.mycursor.rowcount
                print('Inserted: ',count, ' rows at '+ table +',')       
            except sqlite3.Error as error:
                print('Error occured at InsertMajorRecommendation - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.insertMajor()
    
    def createMajorTable(self, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                # query = '''CREATE TABLE IF NOT EXISTS classlist (id TEXT PRIMARY KEY, dept TEXT, title TEXT, number TEXT, score INT);'''
                query = "CREATE TABLE IF NOT EXISTS " +table+ " (name TEXT);"
                self.mycursor.execute(query)
                # self.mycursor.commit()
                print('CreatedTable: ', table)
            except sqlite3.Error as error:
                print('Error occured at Creating Table ' + table+' - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.createMajorTable()
    
    def getTopMajor(self, table):
        try:
            topCourse = None
            self.lock.acquire(True)
            self.connectDatabase()
            self.mycursor.execute('SELECT COUNT(name) as Number, name FROM describeMajor GROUP BY name ORDER BY Number DESC LIMIT 1;')
            data = self.mycursor.fetchone()
            if(data):
               topCourse = data[1]
               print("////////////////////////////")
               print("Top couse is: ", topCourse)      
               print("////////////////////////////")      
            else:
                print('Could not get top Major. Data Dump: ', len(data))    
        except sqlite3.Error as error:
            print('Error occured at Top Major - ', error)      
        finally:
            self.lock.release()
            self.closeConnection()
            return topCourse

    # Visitors Section
    def insertVisitor(self, data, table):
        count = 0
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                self.mycursor.execute('''INSERT INTO visitors VALUES(?, ?, ?, ?, ?);''', (data["city"],data["region"],data["country"],data["postal"],data["timezone"]))
                self.sqlConnection.commit()
                count = self.mycursor.rowcount
                print('Inserted: ',count, ' rows at '+ table +'.')    
            except sqlite3.Error as error:
                print('Error occured at InsertVisitor - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.insertVisitor()

    def createVisitorTable(self, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                query = '''CREATE TABLE IF NOT EXISTS visitors (city TEXT, region TEXT, country TEXT, zip TEXT, timezone TEXT);'''
                self.mycursor.execute(query)
                # self.mycursor.commit()
                print('CreatedTable: ', table)
            except sqlite3.Error as error:
                print('Error occured at Creating Table ' + table+' - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.createTable()

    def getVisitorCityInfo(self, table):
        returnDict = dict()
        try:
            self.lock.acquire(True)
            self.connectDatabase()
            tableSize = self.getAllVisitors('Visitors')
            self.mycursor.execute('''SELECT zip, region, city, COUNT(*) FROM visitors GROUP BY city''')
            data = self.mycursor.fetchall()
            if(len(data) > 0):
                print('Top Cities from', table, '\n')
                for row in data:
                    print('Zip: ', row[0])
                    print('Region: ', row[1])
                    print('City: ', row[2])
                    print('Count: ', row[3])
                    percent = (tableSize/row[3])*100
                    print(percent , '%' , ' live in' , row[2],',', row[1])
                    returnDict["zip"] = row[0]
                    returnDict["city"] = row[2]
                    returnDict["cityPercentage"] = str(floor(percent)) + '%'
                    returnDict["region"] = row[1]
                    returnDict["cityMessage"] = percent , '%' , ' live in' , row[2],',', row[1]
                    return returnDict
            else:
                print('Size is ', len(data))   
        except sqlite3.Error as error:
            print('Error occured at getting visitor data from database - ', error)      
        finally:
            self.lock.release()
            self.closeConnection()
    
    def getAllVisitors(self, table):
        try:
            self.connectDatabase()
            self.mycursor.execute('''SELECT * FROM visitors''')
            data = self.mycursor.fetchall()
            tableSize = len(data)
            return tableSize 
        except sqlite3.Error as error:
            print('Error occured at getting visitor data from database - ', error)      
    
    def getAllVisitorData(self):
        try:
            self.lock.acquire(True)
            self.connectDatabase()
            self.mycursor.execute('''SELECT * FROM visitors''')
            data = self.mycursor.fetchall()
            if(len(data) > 0):
                for row in data:
                    print(row)
            else:
                print('Size is ', len(data))   
        except sqlite3.Error as error:
            print('Error occured at getting visitor data from database - ', error)      
        finally:
            self.lock.release()
            self.closeConnection()
    #Form Section
    def createFormTable(self,table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                # query = '''CREATE TABLE IF NOT EXISTS contact (id TEXT PRIMARY KEY, dept TEXT, title TEXT, number TEXT, score INT);'''
                query = '''CREATE TABLE IF NOT EXISTS contact (id INT PRIMARY KEY, name TEXT, email TEXT, phone TEXT, contactchoice TEXT, notes TEXT, timestamp TEXT, completed INT);'''
                self.mycursor.execute(query)
                print('CreatedTable: ', table)
            except sqlite3.Error as error:
                print('Error occured at Creating Table ' + table+' - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.createFormTable("contact")
    
    def insertForm(self, form):
        count = 0
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                self.mycursor.execute('''INSERT INTO contact VALUES(?,?,?,?,?,?,?,?);''', (form.id,form.name,form.email,form.phoneNumber,form.contactChoice,form.notes,form.timeStamp,form.completed))
                self.sqlConnection.commit()
                count = self.mycursor.rowcount
                print('Inserted: ',count, ' rows at contact.')    
            except sqlite3.Error as error:
                print('Error occured at insert contact form - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.insertForm(form)
    
    def markFromComplete(self,formId):
        if self.sqlConnection:
            try:
                self.lock.acquire(True)
                self.connectDatabase()
                self.mycursor.execute('''UPDATE contact SET completed = 1 WHERE id = ? ''' ,(formId,))
                self.sqlConnection.commit()
                print('Commited')
            except sqlite3.Error as error:
                print('Error occured at Increment - ', error) 
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            print('Cannot mark form as completed.')
    
    def executeDataQuery(self, table):
        if self.sqlConnection:
            try:
                query ="SELECT * FROM contact ORDER BY completed ASC, timestamp DESC";
                self.lock.acquire(True)
                self.connectDatabase()
                self.mycursor.execute(query)
                data = self.mycursor.fetchall()
                if len(data) < 1:
                    print(table +' table is empty')
                else:
                    self.sqlConnection.commit()
                    return data
            except sqlite3.Error as error:
                print('Error Retrieving Data table: ', table)
                print('Error occured  - ', error)  
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            self.connectDatabase()
            self.executeDataQuery()
#Feedback section
    def createFeedbackTable(self, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                # query = '''CREATE TABLE IF NOT EXISTS classlist (id TEXT PRIMARY KEY, dept TEXT, title TEXT, number TEXT, score INT);'''
                query = "CREATE TABLE IF NOT EXISTS " +table+ " (id INT, dept TEXT, title TEXT, number TEXT, feedback INT);"
                self.mycursor.execute(query)
                # self.mycursor.commit()
                print('CreatedTable: ', table)
            except sqlite3.Error as error:
                print('Error occured at Creating Table ' + table+' - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.createFeedbackTable()
    
    def insertFeedback(self, courses, table,feedback):
        if self.sqlConnection:
            try:
                self.lock.acquire(True)
                self.connectDatabase()
                courseId = random.randint(100000,999999)
                for course in courses:
                    self.insertSingleFeedback(course, table, feedback, courseId)
            except sqlite3.Error as error:
                print('Error occured at insertFeedback - ', error)  
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            self.connectDatabase()
            self.insertFeedback()

    def insertSingleFeedback(self, course, table, feedback, courseId):
        count = 0
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.mycursor.execute("INSERT INTO " + table + " VALUES(?, ?, ?, ?, ?);", (courseId, course['course_dept'], course['course_title'], course['course_number'], feedback))
                count += self.mycursor.rowcount
                self.sqlConnection.commit()
                print('Inserted: ',count, ' rows at '+ table +',')    
            except sqlite3.Error as error:
                courseId = course['course_dept'] + course['course_number']
                print('Error occured at InsertSingleFeedback - ', error)  
                print('Failed to insert: - ', courseId)  
            finally:
                self.closeConnection()
        else:
            self.connectDatabase()
            self.insertSingleFeedback()