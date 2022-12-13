# trusted-middleware

## Local Environment Setup
```bash
sudo pip install -r requirements.txt
```

## Docker Setup
```bash
docker build -t trusted_middleware:latest .
docker run --name trusted_middleware -d -p 8000:5000 trusted_middleware:latest
```