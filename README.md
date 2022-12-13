# trusted-middleware

## Local Environment Setup
```bash
sudo pip install -r requirements.txt
```

## Docker Setup
```bash
docker build -t microblog:latest .
docker run --name microblog -d -p 8000:5000 microblog:latest
```