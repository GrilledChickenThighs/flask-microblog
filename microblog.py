from app import server, db
from app.models import User, Post

@server.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}