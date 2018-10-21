from storage import ComicManagerAlchemy
from models import Comic

cm_lite = ComicManagerAlchemy('sqlite:///foxtrot.db')
cm_mysql = ComicManagerAlchemy('mysql://gregoria:moomie11@gregoria.mysql.pythonanywhere-services.com/gregoria$foxtrot')

with cm_lite.session_scope() as s_lite:
    comics = s_lite.query(Comic)
    with cm_mysql.session_scope() as s_my:
        for comic in comics:
            s_lite.expunge(comic)
            s_my.add(comic)
