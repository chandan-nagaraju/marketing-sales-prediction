from flask import Flask, render_template, request, url_for
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn
import os
from sklearn.preprocessing import StandardScaler
folder = os.path.join('static', 'image')

app = Flask(__name__)
model = pickle.load(open('xgboost_regression_model.pkl', 'rb'))
app.config['UPLOAD_FOLDER']=folder
pic = os.path.join(app.config['UPLOAD_FOLDER'], 'OIP.jpg')

@app.route("/", methods=['Get', 'POST'])
def Home():
    return render_template('index.html', name=pic)


standard_to = StandardScaler()
@app.route("/predict",methods=['Post'])


def predict():
    prod_cd = np.arange(1,87)
    slsman_cd = np.arange(1,226)
    slsman_cd = np.delete(slsman_cd, 71)
    if request.method == 'POST':
        PROD_CD = int(request.form['PROD_CD'])
        SLSMAN_CD = int(request.form['SLSMAN_CD'])
        PLAN_MONTH = request.form['PLAN_MONTH']
        if(PLAN_MONTH == 'January'):
            PLAN_MONTH = 1
        elif(PLAN_MONTH == 'February'):
            PLAN_MONTH = 2
        elif (PLAN_MONTH == 'March'):
            PLAN_MONTH = 3
        elif (PLAN_MONTH == 'April'):
            PLAN_MONTH = 4
        elif (PLAN_MONTH == 'May'):
            PLAN_MONTH = 5
        elif (PLAN_MONTH == 'June'):
            PLAN_MONTH = 6
        elif (PLAN_MONTH == 'July'):
            PLAN_MONTH = 7
        elif (PLAN_MONTH == 'August'):
            PLAN_MONTH = 8
        elif (PLAN_MONTH == 'September'):
            PLAN_MONTH = 9
        elif (PLAN_MONTH == 'October'):
            PLAN_MONTH = 10
        elif (PLAN_MONTH == 'November'):
            PLAN_MONTH = 11
        else:
            PLAN_MONTH = 12
        PLAN_YEAR = int(request.form['PLAN_YEAR'])
        if PROD_CD in prod_cd:
            if SLSMAN_CD in slsman_cd:
                df=pd.DataFrame([[PROD_CD,SLSMAN_CD,PLAN_MONTH,PLAN_YEAR]], columns=['PROD_CD', 'SLSMAN_CD', 'PLAN_MONTH', 'PLAN_YEAR'])
                prediction = int(model.predict(df))
                output = prediction + add_hike(prediction)
                if output<0:
                    return render_template('index.html',prediction_text="Sorry the Salesman cannot sell this Product", name=pic)
                else:
                    return render_template('index.html',prediction_text="This Salesman Can Sell The Product with Target {}".format(output), name=pic)
            else:
                return render_template('index.html',prediction_text="Sorry Salesman Code is not valid", name=pic)
        else:
            return render_template('index.html', prediction_text="Sorry Product Code is not valid", name=pic)
    else:
        return render_template('index.html', name=pic)

def add_hike(predicted_output):
    HIKE = int(request.form['Hike'])
    return int((predicted_output / 100) * HIKE)

if __name__=="__main__":
    app.run(debug=True)
