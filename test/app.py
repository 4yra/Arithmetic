from flask import Flask, render_template, jsonify

app = Flask('__name__')

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/test/')
def test():
    return jsonify({'Test': 'test'})

if __name__ == '__main__':
    app.run(debug=True, port=8000 )