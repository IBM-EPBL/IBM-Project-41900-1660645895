from flask import Flask, render_template, request
import requests
import json


API_KEY = "p0ViRMz0B7GX-FBL0VYl3rElxB0qVxl26xM38C_ckbWs"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__, static_url_path='')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkEligibility')
def checkEligibility():
    return render_template('Demo2.html')

@app.route('/predict', methods=['POST'])
def predict():
    greScore = int(request.form['greScore'])
    toeflScore = int(request.form['toeflScore'])
    univRank = int(request.form['univRank'])
    sop = float(request.form['sop'])
    lor = float(request.form['lor'])
    cgpa = float(request.form['cgpa'])
    research = int(request.form['research'])
    array_of_input_fields = ['greScore', 'toeflScore', 'univRank', 'sop', 'lor', 'cgpa', 'research']
    array_of_values_to_be_scored = [greScore, toeflScore, univRank, sop, lor, cgpa, research]
    payload_scoring = {"input_data": [{"field": [array_of_input_fields], "values": [array_of_values_to_be_scored]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5795f5cf-7316-450f-9d9c-f4e025e50210/predictions?version=2022-11-18', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    prediction = predictions['predictions'][0]['values'][0][0]
    

    if (int(prediction[0]*100)>0):
        return render_template('chance.html')
    else:
        return render_template('noChance.html')


if __name__ == "__main__":
    app.run()
