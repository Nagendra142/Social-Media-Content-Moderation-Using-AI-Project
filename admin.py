# from flask import Flask, render_template
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'junk'

# mysql = MySQL(app)

# try:
#     mysql.connection.cursor()
# except Exception as e:
#     print("Error:", e)

# @app.route('/')
# def check():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM dept")
#         fetchdata = cur.fetchall()
#         cur.close()
#         return render_template('Add.html', data=fetchdata)
#     except Exception as e:
#         print(e)
#         return "error"

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.contentModeration  # Create or connect to the 'junk' database

# Define collection
dept_collection = db.adminData  # Collection named 'dept'

# @app.route('/')
def adminData():
    fetchdata = dept_collection.find()
    # if(fetchdata.length!=0):
    #     print("fetched")
    
    print(type(fetchdata))
    fetchdata=list(fetchdata)
    print(type(fetchdata))
    for i in fetchdata:
        print(i)
    return fetchdata

def Delete(value):
    dept_collection.delete_one({'name':value})
    fetchedData=adminData()
    return fetchedData

def addBadWord(data):
    finalData={'name':data}
    dept_collection.insert_one(finalData)

if __name__ == '__main__':
    app.run(debug=True)
