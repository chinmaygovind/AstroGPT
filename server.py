from flask import *  
import secrets
import asyncio
import os
from multiprocessing import Process, Manager
from findImage import *
from pathlib import Path

app = Flask(__name__, static_folder='static')
# Explicit route to serve static files (if default does not work)
@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.static_folder, filename)

queries = {}

@app.route('/')   
def main():   
    return render_template("index.html")   

@app.route('/create-search', methods = ['POST'])   
def create_search():   
    print("DEBUG: /create-search route called")
    if request.method == 'POST':   
        print("DEBUG: POST request received")
        try:
            f = request.files['image-input']
            print(f"DEBUG: File received: {f.filename}")
            
            requestID = secrets.token_urlsafe(30*3//4)
            print(f"DEBUG: Generated requestID: {requestID}")
            
            # Ensure the queryimages directory exists
            query_dir = "static/queryimages"
            if not os.path.exists(query_dir):
                os.makedirs(query_dir)
                print(f"DEBUG: Created directory: {query_dir}")
            
            filename = f"static/queryimages/image_{requestID}.png"
            f.save(filename)   
            print(f"DEBUG: File saved to: {filename}")
            
            # Verify the file was saved
            if os.path.exists(filename):
                print(f"DEBUG: File exists and size: {os.path.getsize(filename)} bytes")
            else:
                print(f"DEBUG: ERROR - File was not saved: {filename}")
                return "Error: Could not save uploaded file", 500
            
            print("DEBUG: About to call queryImage...")
            queries[requestID] = asyncio.run(queryImage(filename))
            print("DEBUG: queryImage completed")
            print(f"DEBUG: Query result: {queries[requestID]}")
            
            print("DEBUG: About to render results template")
            return render_template('results.html', myRequestID=requestID)
        except Exception as e:
            print(f"DEBUG: Exception in create_search: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}", 500
    else:
        print("DEBUG: Non-POST request received")
        return "Method not allowed", 405
 

@app.route('/check-search', methods = ['GET'])   
def check_search():   
    if request.method == 'GET':   
        try:
            requestID = request.args.get("requestID", default=None)
            if queries[requestID] is None:
                data = {"status": "loading"}
                return data, 200
            else:
                data = {"status": "finished"}
                return data, 200
        except Exception as e:
            print("Error: " + str(e))
            return render_template("error.html")

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html', myRequestID=request.args.get("requestID", default=None))

@app.route('/fetch-results', methods= ['GET'])
def fetch_results():
    if request.method == 'GET':   
        requestID = request.args.get("requestID", default=None)
        data = []
        for image in queries[requestID]:
            entry = {}
            entry["title"] = image[:image.index('_')]
            entry["image"] = imageDir + entry["title"].replace(" ", "_") + "/" + image
            entry["hasLink"] = False
            hrefDir = pagesDir + entry["title"].replace(" ", "_") + "/" + image.replace(".png", ".html")
            hrefDir = hrefDir[:-8] + "page_" + hrefDir[-8:]
            print(hrefDir)
            try:
                if os.path.isfile(hrefDir):
                    entry["hasLink"] = True
                    entry["href"] = hrefDir
            except Exception as e:
                print(e)
                entry["href"] = None
            entry["description"] = "This is a deep space object!"
            data.append(entry)
        return jsonify(data)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

