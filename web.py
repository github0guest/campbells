from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from storage import ComicManager

app = Flask(__name__)
CORS(app)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/json/characters/')
def json_characters():
    date = request.args.get('date')
    cm = ComicManager('foxtrot.db')
    return jsonify(cm.characters_from_date(date))


@app.route('/json/dates/')
def json_dates():
    character = request.args.get('character')
    cm = ComicManager('foxtrot.db')
    return jsonify(cm.dates_from_character(character))


@app.route('/json/search/', methods=['POST'])
def search():
    content = request.get_json(force=True)
    cm = ComicManager('foxtrot.db')
    try:
        return jsonify(cm.search_transcripts(content['text']))
    except KeyError as err:
        print(err)
        raise InvalidUsage('KeyError', status_code=400)


if __name__ == '__main__':
    app.run(debug=True)