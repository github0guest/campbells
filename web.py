import logging
from flask_sqlalchemy import SQLAlchemy
from exceptions import NonexistentComicException, NotImplementedException
from flask import jsonify, request, Response
from flask_cors import CORS
from storage import ComicManager
from app import app


CORS(app)
logging.basicConfig(format='%(asctime)s %(message)s')


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
    cm = ComicManager()
    try:
        dates = cm.search_transcripts(content['text'])
    except NotImplementedException as ex:
        logging.exception(ex)
        raise HTTPError(501)
    output = []
    for date in dates:
        filename = date.strftime('%Y-%m-%d')
        display_name = date.strftime('%A, %B %d, %Y')
        output.append({'filename': filename, "display_name": display_name})
    return jsonify(output)


@app.route('/json/comic/next')
def json_next_comic():
    current_date = request.args.get('current_date')
    cm = ComicManager()
    try:
        date = cm.get_next_comic(current_date)
    except NonexistentComicException as ex:
        logging.exception(ex)
        raise HTTPError(204)
    return jsonify(date.strftime('%Y-%m-%d'))


@app.route('/json/comic/previous')
def json_previous_comic():
    current_date = request.args.get('current_date')
    cm = ComicManager()
    try:
        date = cm.get_previous_comic(current_date)
    except NonexistentComicException as ex:
        logging.exception(ex)
        raise HTTPError(204)
    return jsonify(date.strftime('%Y-%m-%d'))


if __name__ == '__main__':
    app.run(debug=True)
