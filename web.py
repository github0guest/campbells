from flask import Flask, jsonify, render_template
from flask_cors import CORS
from storage import ComicManager

app = Flask(__name__)
CORS(app)


@app.route('/json/characters/<date>')
def json_characters(date):
    cm = ComicManager('foxtrot.db')
    return jsonify(cm.characters_from_date(date))


@app.route('/json/dates/<character>')
def json_dates(character):
    cm = ComicManager('foxtrot.db')
    return jsonify(cm.dates_from_character(character))


@app.route('/json/search/<search_term>')
def search(search_term):
    cm = ComicManager('foxtrot.db')
    return jsonify(cm.search_transcripts(search_term))


@app.route('/')
def home():
    return render_template(
        'search.html', title='Search')


@app.route('/characters/')
@app.route('/characters/<date>')
def characters(date=None, char=None):
    cm = ComicManager('foxtrot.db')
    if date is not None:
        char = cm.characters_from_date(date)
    return render_template('characters.html', date=date, char=char, title="Which characters?")


if __name__ == '__main__':
    app.run(debug=True)