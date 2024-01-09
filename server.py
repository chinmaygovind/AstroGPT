from distutils.log import debug 
from fileinput import filename 
from flask import *  
app = Flask(__name__)


@app.route('/')   
def main():   
    return render_template("index.html")   
  
@app.route('/create-search', methods = ['POST'])   
def create_search():   
    if request.method == 'POST':   
        try:
            print(request.files)
            f = request.files['image-input']
            return render_template("error.html")
            #f = request.files['image-input'] 
            #f.save("queryimages/test.png")   
            #return render_template("loading.html", name = f.filename)   
        except Exception as e:
            print("Error: " + str(e))
            return render_template("error.html")
        
if __name__ == '__main__':
    app.run(debug=True)