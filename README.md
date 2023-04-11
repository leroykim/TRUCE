# TRUCE: Trusted Compliance Enforcement Framework.

## Local Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
sudo pip install -r requirements.txt
```

## Docker Setup
```bash
docker build -t trusted_middleware:latest .
docker run --name trusted_middleware -d -p 8000:5000 trusted_middleware:latest
```