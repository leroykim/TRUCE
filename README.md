# 🤝 TRUCE: Trusted Compliance Enforcement Framework.
[![KnAcc Lab](https://tinyurl.com/knacclogo)](https://knacc.umbc.edu/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

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