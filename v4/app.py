from flask import Flask, jsonify, render_template, request, redirect, url_for
import urllib.request
from PIL import Image
import base64
import io
import numpy as np
import pickle
import cv2
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.models import load_model
from numpy import loadtxt
import math
import random
from csv import writer
import sqlite3 as sql

def connect():
    con = sql.connect("./db/database.db")
    cur = con.cursor()
    return con, cur

def insert_score(score):
    con, cur = connect()
    cur.execute('INSERT INTO games_played (score) VALUES (?)', (score,))
    con.commit()
    con.close()

def insert_scorebord(name, score):
    con, cur = connect()
    con = sql.connect("./db/database.db")
    cur = con.cursor()
    cur.execute('INSERT INTO scorebord (name, score) VALUES (?,?)', (name, score))
    con.commit()
    con.close()

def highscore():
    con, cur = connect()
    cur.execute("SELECT * FROM scorebord")
    rows = dict(cur.fetchall())
    con.close()
    keys = list(rows.keys())
    values = list(rows.values())
    sorted_value_index = np.argsort(values)
    player_score = [values[i] for i in sorted_value_index][-3:len(sorted_value_index)]
    player_name  = [keys[i] for i in sorted_value_index][-3:len(sorted_value_index)]
    return player_score, player_name

from crop_img import Crop

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('game.html')

model = load_model('./ML_models/cnn.h5')
@app.route('/predict/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
       req = request.get_json()
    
    url = req['link']

    def pred_img(img_b64):
        decode_img = base64.b64decode(img_b64)
        image = Image.open(io.BytesIO(decode_img))
        image_np = np.array(image)
        img_crop = np.array(image.crop(Crop(image_np).w_h()))
        # decode_img = base64.b64decode(img_b64)
        # image = Image.open(io.BytesIO(decode_img))
        # img_crop = image.crop(w_h(image))
        # image_np = np.array(img_crop)
        if np.argmin(img_crop) == 0:
            return 'no number'
        else:
            gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
            img_resize = cv2.resize(gray, (28,28), interpolation=cv2.INTER_LINEAR)
            img_resize = cv2.bitwise_not(img_resize)
            img_resize = img_resize.reshape(784,) / 255.0
            img_resize = img_resize.reshape(-1,28,28,1)
            pred = int(np.argmax(model.predict(img_resize), axis=-1)[0])
            return pred

    pred = pred_img(url)
    print(f'\n{pred}\n')

    return jsonify({'resp': pred}), 200


from expression import *
@app.route('/expression/<score>', methods=['POST', 'GET'])
def get_expression(score):
    score = int(score)
    # Level 1
    if score > -1 and score < 5:
        expression = exp.eazy(exp.add(), exp.sub())
    # Level 2
    elif score >=5 and score < 10:
        expression = exp.eazy(exp.add_and_sub(), exp.sub_and_add())
    # Level 3
    elif score >=10 and score < 20:
        expression = exp.eazy(exp.multi_and_add(), exp.multi_and_sub())
    # Level 4
    elif score >=20 and score < 30:
        expression = exp.eazy(exp.div_and_add(), exp.div_and_sub())
    # Level 5
    elif score >= 30:
        expression = exp.hard()

    print(f'\n{expression[1]}')
    print(f'{expression[0]}\n')
    return jsonify({'string': expression[0], 'expression':expression[1], 'sum': expression[2]}), 200

@app.route('/gameover/',  methods=['POST', 'GET'])
def go():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        insert_scorebord(name,score)
        player_score, player_name = highscore()
        print(player_score, player_name)
    return render_template('score_board.html', score_count=score, player_name= str(player_name)[1:-1], player_score=str(player_score)[1:-1], hide = 'hide')

@app.route('/scoreboard/<score>', methods=['POST', 'GET'])
def scoreboard(score):

    player_score, player_name = highscore()
    insert_score(score)
    return render_template('score_board.html', score_count=score, player_name= str(player_name)[1:-1], player_score=str(player_score)[1:-1])

@app.route('/new_game/', methods=['POST', 'GET'])
def new_game():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8000 )