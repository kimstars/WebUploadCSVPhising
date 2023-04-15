#importing required libraries

from flask import Flask, request, render_template,jsonify
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
warnings.filterwarnings('ignore')


import json
from pandas import json_normalize

import pickle


import json
from flask import Flask, render_template, url_for, request, redirect, abort
import os
from flask.helpers import flash
from werkzeug.utils import secure_filename

# Ramdonforest

from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.secret_key = "doan"
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.doc', '.docx','.csv']
socketio = SocketIO(app)

cwd = os.getcwd()
FILES_FOLDER = os.path.join(cwd, 'files')
app.config['FILES_FOLDER'] = FILES_FOLDER


@socketio.on('connect')
def on_connect():
    print('Client connected')
    


@app.route("/")
def index():
    # return render_template("index.html", xx= -1)
    return render_template("new.html")


# nhận 1 url
@app.route("/get_url", methods= ["POST"])
def get_url():
    try:
        if request.method == 'POST':
            text_url = request.values.get('url')
            print("co dua test => ", text_url)
            if text_url != None:
                # xử lý detect url
                # ...
                x = testGBoosting(text_url)

                if x == 1:
                    predict_url = "UNSAFE"
                elif x == 0:
                    predict_url = "SAFE"
                else:
                    predict_url = "SUSPICIOUS"


                data = {
                    "url": text_url,
                    "predict": predict_url
                }
                return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        print("\tError ne kiet", e)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

import threading

# nhận file csv
@app.route("/get_file", methods=["POST"])
def get_file():
    try:
        if request.method == 'POST':
            if request.files:
                f = request.files['file']
                fileName = f.filename
                filename = secure_filename(fileName)
                if filename != '':
                    file_exten = os.path.splitext(filename)[1]
                    if file_exten not in app.config['UPLOAD_EXTENSIONS']:
                        flash("Please upload files with the following extensions: '.txt', '.doc', '.docx'!")
                        abort(400)
                f.save(os.path.join(app.config['FILES_FOLDER'],fileName))
                # đọc file
                # temp_file = 
                df = pd.read_csv("files\\"+filename,names=['url'])


                df["predict"] = ''

                for i in range(len(df)):
                    t = threading.Thread(target=testGBoosting, args=(df['url'].iloc[i],))
                    t.start()
                    
                #     x = testGBoosting(df['url'].iloc[i])
                #     if x == 1:
                #         predict_url = "UNSAFE"
                #     elif x == 0:
                #         predict_url = "SAFE"
                #     else:
                #         predict_url = "SUSPICIOUS"
                #     df['predict'].iloc[i] = predict_url

                # data = df.to_json(orient = "records")
                # data = json.loads(data)
     
                # return json.dumps(data, ensure_ascii=False)
                return jsonify({'message': 'Đã bắt đầu xử lý các item trong file CSV'})
            
    except Exception as e:
        print("\tError", e)
        return redirect(url_for('index'))
    return redirect(url_for('index'))



from pusher import Pusher

pusher = Pusher(app_id="1496129", key="e0f057db90b68cb7a529", secret="95f3c0e4626c0df3d2e7", cluster="ap1")


from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

import datetime

@socketio.on('testGBoosting')
def testGBoosting(url):
    start_time = datetime.datetime.now()
    url = request.form["url"]
    print("co chau test =>", url)
    obj = FeatureExtraction(url)
    print(obj.getFeaturesList())
    
    x = np.array(obj.getFeaturesList()).reshape(1,30) 
    print(x)
    y_pred =gbc.predict(x)[0]
    print(y_pred)
    #1 is safe       
    #-1 is unsafe
    y_pro_phishing = gbc.predict_proba(x)[0,0]
    y_pro_non_phishing = gbc.predict_proba(x)[0,1]
    # if(y_pred ==1 ):
    pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
    print(pred)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time

    print(f"Thời gian chạy của {url} là {elapsed_time}" )
    xx =round(y_pro_non_phishing,2)
    return xx
    


if __name__ == "__main__":
    socketio.run(app)
    # app.run(host='0.0.0.0', port=3400, debug=True)