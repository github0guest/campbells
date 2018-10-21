from storage import ComicManager
from models import Comic

cm_lite = ComicManager('sqlite:///foxtrot.db')
cm_mysql = ComicManager('mysql://gregoria:moomie11@gregoria.mysql.pythonanywhere-services.com/gregoria$foxtrot?charset=utf8')

with cm_lite.session_scope() as s_lite:
    comics = s_lite.query(Comic)
    with cm_mysql.session_scope() as s_my:
        for comic in comics:
            new_comic = Comic(date=comic.date, transcript=comic.transcript)
            s_my.add(new_comic)
