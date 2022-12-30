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


num = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
# Leval 1 -------------------
def leval_1():
    sum = 10
    while sum > 9:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] != 0:
            sum = n[0] + n[1]
    expression = f'{n[0]} + {n[1]}'
    string = f'{num[n[0]]} plus {num[n[1]]}'
    return string, expression, sum

# Leval 2 -------------------
def level_2():
    sum = -1
    while sum < 0:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] != 0:
            sum = n[0] - n[1]
    expression = f'{n[0]} - {n[1]}'
    string = f'{num[n[0]]} minus {num[n[1]]}'
    return string, expression, sum

# Leval 3 -------------------
def level_3():
    add_or_sum = math.floor(random.random()* 10)
    if add_or_sum < 4.5:
        return leval_1()
    else:
        return level_2()

# Leval 4 -------------------
def level_4():
    sum = -1
    while sum < 0 or sum > 9:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] and n[2] != 0:
            sum = n[0] - n[1] + n[2]
    expression = f'{n[0]} - {n[1]} + {n[2]}'
    string = f'{num[n[0]]} minus {num[n[1]]} plus {num[n[2]]}'
    return string, expression, sum

# Leval 5 -------------------
def div_and_add():
    sum = -1
    while sum < 0 or sum > 9:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] and n[2] != 0 and n[1] != 1:
            if n[0] % n[1] == 0 and n[0] != n[1]:
                sum = n[0] / n[1] + n[2]
    expression = f'{n[0]} / {n[1]} + {n[2]}'
    string = f'{num[n[0]]} divided by {num[n[1]]} plus {num[n[2]]}'
    return string, expression, sum

def div_and_sub():
    sum = -1
    while sum < 0 or sum > 9:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] and n[2] != 0 and n[1] != 1:
            if n[0] % n[1] == 0 and n[0] != n[1]:
                sum = n[0] / n[1] - n[2]
    expression = f'{n[0]} / {n[1]} - {n[2]}'
    string = f'{num[n[0]]} divided by {num[n[1]]} minus {num[n[2]]}'
    return string, expression, sum

def level_5():
    add_or_sum = math.floor(random.random()* 10)
    if add_or_sum < 4.5:
        return div_and_add()
    else:
        return div_and_sub()

# Leval 6 -------------------
def multi_and_add():
    sum = -1
    while sum < 0 or sum > 9:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] and n[2] != 0:
            if n[0] != 1 and n[1] != 1:
                sum = n[0] * n[1] + n[2]
    expression = f'{n[0]} x {n[1]} - {n[2]}'
    string = f'{num[n[0]]} times {num[n[1]]} plus {num[n[2]]}'
    return string, expression, sum

def multi_and_sub():
    sum = -1
    while sum < 0 or sum > 9:
        n = [math.floor(random.random()* 10) for i in range(0,3)]
        if n[0] and n[1] and n[2] != 0:
            if n[0] != 1 and n[1] != 1:
                sum = n[0] * n[1] - n[2]
    expression = f'{n[0]} x {n[1]} - {n[2]}'
    string = f'{num[n[0]]} times {num[n[1]]} minus {num[n[2]]}'
    return string, expression, sum

def level_6():
    add_or_sum = math.floor(random.random()* 10)
    if add_or_sum < 4.5:
        return multi_and_add()
    else:
        return multi_and_sub()

# Crop images begfore prediction
def top_crop(img_size, img_array):
    for i in range(0, img_size[0]):
        if np.amin(img_array[i]) < 255:
            return i - 10
def bottom_crop(img_size, img_array):
    for i in range(img_size[0]-1, 0, -1):
        if np.amin(img_array[i]) < 255:
            return i + 10
def left_crop(img_size, img_array):
    for i in range(0, img_size[0]):
        for b in range(0, img_size[0]):
            if np.mean(img_array[b][i]) < 255:
                return i - 10
def right_crop(img_size, img_array):
    for i in range(img_size[0]-1, 0, -1):
        for b in range(0, img_size[0]):
            if np.mean(img_array[b][i]) < 255:
                return i + 10

def w_h(img):
    img_size = img.size
    img_array = np.asarray(img)
    l = left_crop(img_size, img_array)
    t = top_crop(img_size, img_array)
    r = right_crop(img_size, img_array)
    b = bottom_crop(img_size, img_array)
    if None not in [l,t,r,b]:
        height = b - t
        width = r - l
        if height < width:
            x = (width - height) / 2
            return l, math.floor(t-x), r, math.floor(b+x)
        else:
            x = (height - width) / 2
            return math.floor(l-x), t, math.floor(r+x), b
    else:
        return 0, 0, 300, 300



app = Flask(__name__)
@app.route('/')
def home():
    return render_template('game.html')

# model = pickle.load(open('mnist_model.sav', 'rb'))
# @app.route('/predict/', methods=['POST', 'GET'])
# def predict():
#     if request.method == 'POST':
#        req = request.get_json()
#     url = req['link']

#     def load_img(img_b64):
#         decode_img = base64.b64decode(img_b64)
#         image = Image.open(io.BytesIO(decode_img))
#         image_np = np.array(image)
#         gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#         img_resize = cv2.resize(gray, (28,28), interpolation=cv2.INTER_LINEAR)
#         img_resize = cv2.bitwise_not(img_resize)
#         return img_resize

#     img = load_img(url)
#     pred = int(model.predict(img.reshape(1, -1))[0])
#     print(pred)

#     return jsonify({'resp': pred}), 200

model = load_model('./ML_models/cnn.h5')
@app.route('/predict/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
       req = request.get_json()
    
    url = req['link']
    # print(url)

    def pred_img(img_b64):
        decode_img = base64.b64decode(img_b64)
        image = Image.open(io.BytesIO(decode_img))
        img_crop = image.crop(w_h(image))
        image_np = np.array(img_crop)
        if np.argmin(image_np) == 0:
            return 'no number'
        else:
            gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            img_resize = cv2.resize(gray, (28,28), interpolation=cv2.INTER_LINEAR)
            img_resize = cv2.bitwise_not(img_resize)
            img_resize = img_resize.reshape(784,) / 255.0
            img_resize = img_resize.reshape(-1,28,28,1)
            pred = int(np.argmax(model.predict(img_resize), axis=-1)[0])
            return pred

    pred = pred_img(url)
    print(f'\n{pred}\n')

    return jsonify({'resp': pred}), 200

@app.route('/expression/<level>', methods=['POST', 'GET'])
def get_expression(level):
    level = int(level)
    if level == 1:
        expression = leval_1()
    elif level == 2:
        expression = level_2()
    elif level == 3:
        expression = level_3()
    elif level == 4:
        expression = level_4()
    elif level == 5:
        expression = level_5()
    elif level == 6:
        expression = level_6()

    print(f'\n{expression[1]}')
    print(f'{expression[0]}\n')
    return jsonify({'string': expression[0], 'expression':expression[1], 'sum': expression[2]}), 200

@app.route('/gameover/',  methods=['POST', 'GET'])
def go():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        # email = request.form['email']
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