from flask import Flask, render_template, session, redirect, url_for, request
import requests
import random

WORD_LIST = "wordlist.txt"

app = Flask(__name__)
app.secret_key = 'test_environment'
# API_URL = 'https://random-word-api.herokuapp.com/word?number=1'

def get_random_word(word_file, min_word_length):
    # response = requests.get(API_URL)
    # if response.status_code == 200:
    #     return response.json()[0].upper()
    # print("Request to get a random word failed...")
    # return None
    """Get a random word from the wordlist using no extra memory"""
    num_words_processed = 0
    curr_word = None
    with open(word_file, 'r') as f:
        for word in f:
            if '(' in word or ')' in word:
                continue
            word = word.strip().upper()
            if len(word) < min_word_length:
                continue
            num_words_processed += 1
            if random.randint(1, num_words_processed) == 1:
                curr_word = word
    return curr_word

@app.route('/reset')
def reset():
    session.pop('word', None)
    session.pop('guesses', None)
    session.pop('misses', None)
    session.pop('message', None)
    return redirect(url_for('index'))

@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess'].upper()
    if guess not in session['guesses']:
        session['guesses'].append(guess)
        if guess in session['word']:
            session['message'] = f"Good Guess! {guess} is in the word!"
        else:
            session['misses'] += 1
            session['message'] = f"Sorry! {guess} is not in the word!"
    else:
        session['message'] = f"You already guessed '{guess}'."
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'word' not in session:
        session['word'] = get_random_word(WORD_LIST, 5)
        session['guesses'] = []
        session['misses'] = 0
        session['message'] = ''
    word_display = ''.join([letter if letter in session['guesses'] else '_ ' for letter in session['word']])
    return render_template('index.html', word_display=word_display, guesses=session['guesses'], misses=session['misses'],message=session.get('message', ''))


if __name__ == "__main__":
    app.run(debug=True)