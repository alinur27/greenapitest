from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None

    if 'idinstance' not in session:
        session['idinstance'] = ''
    if 'ApiTokenInstance' not in session:
        session['ApiTokenInstance'] = ''

    if request.method == 'POST':
        if 'getSettings' in request.form:
            session['idinstance'] = request.form['idinstance']
            session['ApiTokenInstance'] = request.form['ApiTokenInstance']
            url = f"https://api.green-api.com/waInstance{session['idinstance']}/getSettings/{session['ApiTokenInstance']}"
            response = requests.get(url).text
        elif 'getStateinstance' in request.form:
            session['idinstance'] = request.form['idinstance']
            session['ApiTokenInstance'] = request.form['ApiTokenInstance']
            url = f"https://api.green-api.com/waInstance{session['idinstance']}/getStateInstance/{session['ApiTokenInstance']}"
            response = requests.get(url).text
        elif 'send_message' in request.form:
            phone_number = request.form['phone_number']
            message = request.form['message']
            url = f"https://api.green-api.com/waInstance{session['idinstance']}/sendMessage/{session['ApiTokenInstance']}"
            payload = {
                "chatId": f"{phone_number}@c.us",
                "message": message
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers).text
        elif 'sendFileByUrl' in request.form:
            phone_number = request.form['phone_number']
            file_url = request.form['file_url']
            url = f"https://api.green-api.com/waInstance{session['idinstance']}/sendFileByUrl/{session['ApiTokenInstance']}"
            payload = {
                "chatId": f"{phone_number}@c.us",
                "urlFile": file_url,
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers).text

    return render_template('index.html', response=response, idinstance=session['idinstance'], ApiTokenInstance=session['ApiTokenInstance'])

if __name__ == '__main__':
    app.run(debug=True)
