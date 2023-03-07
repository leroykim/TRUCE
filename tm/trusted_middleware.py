from app import create_app

app = create_app()

# source venv/bin/activate
# docker build -t trusted_middleware:latest .
# docker run --name trusted_middleware -d -p 8000:5000 trusted_middleware:latest