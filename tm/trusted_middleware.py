from app import create_app, db
from app.models import User, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# source venv/bin/activate
# docker build -t trusted_middleware:latest .
# docker run --name trusted_middleware -d -p 8000:5000 trusted_middleware:latest