from flask import Flask, request, render_template, url_for
import requests
import test
import os
import custom_search_01 as cse
app = Flask(__name__)
 
# DETECT_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2/detect'
# TRANSLATE_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2'
# HEADERS = {
#    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
#    'x-rapidapi-key': "6caaf5715emsh2d9a45203b194c0p138b8djsn3e4bdde445d9",
#    'content-type': "application/x-www-form-urlencoded"
#    }


# def test1(): 
#     return '<input type="text" name="key_words>'

# abc = test1()
user = os.getlogin()
@app.route('/')
@app.route('/index')
def index():
   try:
      return render_template('index.html', title='Home', user=user)
   except Exception as e:
      return str(e)


# @app.route('/detect', methods=['POST'])
# def detect():
#    # parse args
#    text = request.form.get('text')
 
#    # url encode text
#    long_list_of_words = text.split(' ')
#    url_encoded_text = f"q={'%20'.join(long_list_of_words)}"
 
#    payload = url_encoded_text
 
#    # make the request
#    r = requests.post(DETECT_BASE_URL, data=payload, headers=HEADERS)
  
#    return r.json()
 
 
@app.route('/search', methods=['POST', 'GET'])
def search():
   try:
      # parse args
      if request.method == 'POST':
         keywords = request.form.get('search')
         listDocs = cse.search('.//test_cases.csv', keywords)
         print('landed in search: ' + keywords)
         return render_template('doc_search.html',title='Search',key_words=keywords,docs=listDocs)
   except Exception as e:
      return str(e)
 

if __name__ == '__main__':
   app.run(debug=True)