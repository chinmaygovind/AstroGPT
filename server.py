from flask import *  
import secrets
from multiprocessing import Process
from findImage import queryImage
import sqlite3
from sqlite3 import Error
import datetime 

app = Flask(__name__)

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

con = create_connection("mydb.sqlite")
cur = con.cursor()

@app.route('/')   
def main():   
    return render_template("index.html")   
  
@app.route('/create-search', methods = ['POST'])   
def create_search():   
    if request.method == 'POST':   
        try:
            print(request.files)
            f = request.files['image-input']
            requestID = secrets.token_urlsafe(30*3//4)
            cur.execute(f"""
    INSERT INTO queries VALUES
        ({requestID}, {None}, {datetime.datetime.now()}),
""")
            f.save(f"queryimages/image_{requestID}.png")   
            heavy_process = Process(target=search_image, args=[requestID], daemon=True)
            heavy_process.start()
            return render_template("loading.html", myRequestID=requestID)   
        
        except Exception as e:
            print("Error: " + str(e))
            return render_template("error.html")

@app.route('/check-search', methods = ['GET'])   
def check_search():   
    if request.method == 'GET':   
        try:
            requestID = request.args.get("requestID", default=None)
            print(requestID)
            print("Queries in check_search: " + str(queries))
            print("Found " + str(queries[requestID]))
            if queries[requestID] is None:
                data = {"status": "loading"}
                return data, 200
            else:
                data = {"status": "finished"}
                return data, 200
        except Exception as e:
            print("Error: " + str(e))
            return render_template("error.html")


def search_image(requestID):
    queries[requestID] = queryImage(f"queryimages/image_{requestID}.png")
    print(f"Processed request {requestID}: " + str(queries[requestID]))
    print("All queries: " + str(queries))

if __name__ == '__main__':
    app.run(debug=True)

