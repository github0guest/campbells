from sqlalchemy import orm
from storage import EmptySearchException
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from storage import ComicManagerAlchemy

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
    cm = ComicManagerAlchemy('sqlite:///foxtrot.db')
    try:
        return jsonify(cm.characters_from_date(date))
    except ValueError as err:
        print(err)
        raise HTTPError(204)
    except orm.exc.NoResultFound as ex:
        print(ex)
        raise HTTPError(204)


@app.route('/json/dates/')
def json_dates():
    character = request.args.get('character')
    cm = ComicManagerAlchemy('sqlite:///foxtrot.db')
    return jsonify(cm.dates_from_character(character))


@app.route('/json/search/', methods=['POST'])
def search():
    content = request.get_json(force=True)
    cm = ComicManagerAlchemy('sqlite:///foxtrot.db')
    try:
        return jsonify(cm.search_transcripts(content['text']))
    except EmptySearchException as ex:
        print(ex)
        raise HTTPError(204)
    except KeyError as err:
        print(err)
        raise HTTPError(401)


@app.route('/json/comic/next')
def json_next_comic():
    current_date = request.args.get('current_date')
    cm = ComicManagerAlchemy('sqlite:///foxtrot.db')
    return jsonify(cm.get_next_comic(current_date))


@app.route('/json/comic/previous')
def json_next_comic():
    current_date = request.args.get('current_date')
    cm = ComicManagerAlchemy('sqlite:///foxtrot.db')
    return jsonify(cm.get_previous_comic(current_date))


if __name__ == '__main__':
    app.run(debug=True)
