"""A trivial spell checking API using Flask and TextBlob.

This app wraps a very simple JSON interface around TextBlob and provides very
basic spell checking and correction support (english only for now).
"""
# third-party imports
from flask import Flask
from flask import jsonify
from flask import request
from textblob import TextBlob
from textblob import Word


# define Flask app that does all the magic
app = Flask(__name__)


@app.route('/correction')
def correction():
    """Simple handler that parses a query parameter and returns a best-guess
    spelling correction using the TextBlob library.

    urls should take the form '/correction?text=some%20textt%20to%20corect'

    data returned will be a JSON object that looks like:
        {text: "some text to correct"}
    """
    text = request.args.get('text', '')
    text = TextBlob(text)
    return jsonify(text=unicode(text.correct()))


@app.route('/spellcheck')
def spellcheck():
    """Handler that provides basic spell-checking of text that is passed in
    via query parameter.

    urls should take the form '/spellcheck?text=my%20speeling%20is%20quite%20badd'

    data returned will be a JSON object that looks like:
        {
            "badd": [
                ["bad", 0.47987616099071206], ["bald", 0.25386996904024767],
                ["band", 0.16718266253869968], ["add", 0.08359133126934984],
                ["bade", 0.015479876160990712]
            ],
            "is": [["is", 1]],
            "my": [["my", 1]],
            "quite": [["quite", 1]],
            "speeling": [["spelling", 0.5], ["speeding", 0.25], ["peeling", 0.25]]
        }
    """
    text = request.args.get('text', '')
    words = {}
    for word in text.split():
        words[word] = Word(word).spellcheck()
    return jsonify(**words)


if __name__ == '__main__':

    # app runs in debug mode, turn this off if you're deploying
    app.run(debug=True)
