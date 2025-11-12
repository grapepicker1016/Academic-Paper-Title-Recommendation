from flask import Flask, request, jsonify, render_template
from generate import recommend, MODEL_PATH
from T5.model import create_model

app = Flask(__name__)
model = create_model(MODEL_PATH, use_cuda=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    st = [str(x) for x in request.form.values()]
    prediction = recommend(model, st[0])
    pr = "1) " + prediction[0][0] + " // " + "2) " + prediction[0][1] + " // " + "3) " +prediction[0][2]
    return render_template('index.html', recommended='Recommended Titles: {}'.format(pr))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = recommend(model, data)

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
