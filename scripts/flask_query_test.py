import os
from flask import Flask, request

app = Flask(__name__)

# Calculate the path to the bad words file (needs absolute path)
script_dir = os.path.dirname(os.path.abspath(__file__))
bad_words_file = os.path.join(script_dir, 'bad_words.txt')

# read through the bad words file and store the words in a set
with open(bad_words_file, 'r') as file:
    content = file.read()
    bad_words = {word.strip().lower() for word in content.split(',')}

# Route to check if a word is bad


@app.route('/queryBad', methods=['GET'])
def queryBad():
    # Get the word from the query string
    word = request.args.get('word').lower()
    # if bad word
    if word in bad_words:
        return 'You entered a bad word!'
    return 'Your word was: {word}'.format(word=word)


if __name__ == '__main__':
    app.run(debug=True)
