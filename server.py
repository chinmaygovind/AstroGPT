from flask import *  
import secrets
from multiprocessing import Process, Manager
from findImage import *
from pathlib import Path

app = Flask(__name__)

queries = {}

@app.route('/')   
def main():   
    return render_template("index.html")   

@app.route('/create-search', methods = ['POST'])   
async def create_search():   
    if request.method == 'POST':   
        f = request.files['image-input']
        requestID = secrets.token_urlsafe(30*3//4)
        f.save(f"static/queryimages/image_{requestID}.png")   
        queries[requestID] = await queryImage(f"static/queryimages/image_{requestID}.png")
        print("Awaiting process...")
        print(queries[requestID])
        return render_template('results.html', myRequestID=requestID)
 

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

