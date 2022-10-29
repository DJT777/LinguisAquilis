import threading
import sqlite3

class database:
    path = ""
    mycursor = None
    sqlConnection = None
    lock = None


    def __init__(self):
        try:
            self.sqlConnection = sqlite3.connect(self.path, check_same_thread=False)
            cursor = self.sqlConnection.cursor()
            self.mycursor = cursor
            self.lock = threading.Lock()
            self.createTable('classlist')
        except sqlite3.Error as error:
            print('Error occured Init - ', error)
    
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

    def createTable(self, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.lock.acquire(True)
                query = '''CREATE TABLE IF NOT EXISTS classlist (id TEXT PRIMARY KEY, dept TEXT, title TEXT, number TEXT, score INT);'''
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

    def insertClass(self, courses, table):
        count = 0
        if self.sqlConnection:
            try:
                # query = 'INSERT or IGNORE INTO classlist VALUES(?, ?, ?, ?);'
                self.connectDatabase()
                self.lock.acquire(True)
                for course in courses:
                    courseId = course['course_dept'] + course['course_number']
                    self.mycursor.execute('''INSERT or IGNORE INTO classlist VALUES(?, ?, ?, ?, ?);''', (courseId, course['course_dept'], course['course_title'], course['course_number'], 1))
                    count += self.mycursor.rowcount
                    self.sqlConnection.commit()
                print('Inserted: ',count, ' rows.')    
            except sqlite3.Error as error:
                print('Error occured at InsertClass - ', error)  
            finally:
                self.closeConnection()
                self.lock.release()
        else:
            self.connectDatabase()
            self.insertClass()
    def dropTable(self, table):
        if self.sqlConnection:
            try:
                self.connectDatabase()
                self.mycursor.execute("DROP TABLE IF EXISTS " +table)
                # self.mycursor.commit()
                print("Dropped: " +table)
            except sqlite3.Error as error:
                print('Error occured at DropTable - ', error)  
            finally:
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
                else:
                    print('All data in table', table, '\n')
                    for row in data:
                        print(row)
                print('Table size is: ', len(data))
                self.sqlConnection.commit()
            except sqlite3.Error as error:
                print('Error Getting Table ', table)
                print('Error occured  - ', error)  
            finally:
                self.lock.release()
                self.closeConnection()
        else:
            self.connectDatabase()
            self.getAllTableData()
    
    def increment(self, courseId):
        if self.sqlConnection:
            try:
                # self.lock.acquire(True)
                self.connectDatabase()
                # print('Course ID: ', courseId)
                self.mycursor.execute('''UPDATE classlist SET score = score + 1 WHERE id = ? ''' ,(courseId,))
                self.sqlConnection.commit()
                print('Commited')
            except sqlite3.Error as error:
                print('Error occured at Increment - ', error) 
            finally:
                # self.lock.release()
                self.closeConnection()
        else:
            print('Cannot increment')
    
    def courseExists(self, course, table):
        try:
            self.lock.acquire(True)
            self.connectDatabase()
            courseId = course['course_dept'] + course['course_number'] 
            # query = 'SELECT * FROM ' + table + ' WHERE id = ' + courseId
            # courseId = "'" + courseId + "'"
            self.mycursor.execute('''SELECT * FROM classlist WHERE id = ?''', (courseId,))
            count = self.mycursor.fetchone() is not None
            print('Id: ',courseId , ' is ' , count)
            if count:
                self.increment(courseId)
            else:
                print('Add')
                courseList = []
                courseList.insert(course)
                self.insertClass(courseList, 'classlist')
        except sqlite3.Error as error:
                print('Error occured at exists - ', error)  
        finally:
            self.lock.release()
            self.closeConnection()

    def getTopCourses(self, table):
        try:
            self.lock.acquire(True)
            self.connectDatabase()
            self.mycursor.execute('''SELECT score, title FROM classlist ORDER BY title DESC LIMIT 5''')
            data = self.mycursor.fetchall()
            if(len(data) > 1):
                print('All data in table', table, '\n')
                for row in data:
                    print(row)
            else:
                print('Table size is ', len(data))    
        except sqlite3.Error as error:
            print('Error occured at Top Courses - ', error)      
        finally:
            self.lock.release()
            self.closeConnection()
        
    


