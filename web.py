from storage import EmptySearchException
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from storage import ComicManager

app = Flask(__name__)
CORS(app)


class HTTPError(Exception):
    def __init__(self, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code


@app.errorhandler(HTTPError)
def handle_http_error(error):
    return Response(status=error.status_code)


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
    except EmptySearchException as ex:
        print(ex)
        raise HTTPError(204)
    except KeyError as err:
        print(err)
        raise HTTPError(401)


if __name__ == '__main__':
    app.run(debug=True)