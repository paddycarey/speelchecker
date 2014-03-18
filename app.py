from flask import Flask
from flask import jsonify
from flask import request
from textblob import TextBlob
from textblob import Word


app = Flask(__name__)


@app.route('/correction')
def correction():
    text = request.args.get('text', '')
    text = TextBlob(text)
    return jsonify(text=unicode(text.correct()))


@app.route('/spellcheck')
def spellcheck():
    text = request.args.get('text', '')
    words = {}
    for word in text.split():
        words[word] = Word(word).spellcheck()
    return jsonify(**words)


if __name__ == '__main__':
    app.run(debug=True)
