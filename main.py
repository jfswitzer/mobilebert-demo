import time
import socketio
import json
from tflite_support.task import text
import logging
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

logging.basicConfig(filename='berty.log', encoding='utf-8', level=logging.DEBUG)
class BertQA():
    def __init__(self):
        self.answerer = text.BertQuestionAnswerer.create_from_file('mobilebert.tflite')
        self.answerer._options.num_threads=2
        self.answerer._options.accelerator_name="google-edgetpu"
    def get_answer(self,question,text):
        bert_qa_result = self.answerer.answer(text,question)
        return bert_qa_result

app = Flask(__name__)
app.config['SECRET_KEY'] = "actualsecret"
socketio = SocketIO(app)
classifier = BertQA()
with open('qa.json') as json_file:
    data = json.load(json_file)
    TITLES = data['titles']
    CONTENTS = data['contents']

@app.route("/jobsubmit/", methods=['POST'])
def job_submit():
    body = request.get_json()
    assert "question" in body
    assert "text" in body
    text = [body["text"]]
    if text in TITLES:
        text=CONTENTS[TITLES.index(text)]
    start = time.time()
    result = classifier.get_answer(body["question"],text[0])
    end = time.time()
    answer = result.answers[0].text
    latency=end-start
    return jsonify(success=True, answer=answer,latency=latency)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0',allow_unsafe_werkzeug=True,debug=True)
