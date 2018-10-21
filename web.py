from storage import NotImplementedException, NonexistentComicException
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from storage import ComicManager
import config

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


@app.route('/json/search/', methods=['POST'])
def search():
    content = request.get_json(force=True)
    cm = ComicManager(config.database)
    try:
        return jsonify(cm.search_transcripts(content['text']))
    except NotImplementedException as ex:
        print(ex)
        raise HTTPError(501)


@app.route('/json/comic/next')
def json_next_comic():
    current_date = request.args.get('current_date')
    cm = ComicManager(config.database)
    try:
        return jsonify(cm.get_next_comic(current_date))
    except NonexistentComicException as ex:
        print(ex)
        raise HTTPError(204)


@app.route('/json/comic/previous')
def json_previous_comic():
    current_date = request.args.get('current_date')
    cm = ComicManager(config.database)
    try:
        return jsonify(cm.get_previous_comic(current_date))
    except NonexistentComicException as ex:
        print(ex)
        raise HTTPError(204)


if __name__ == '__main__':
    app.run(debug=True)
