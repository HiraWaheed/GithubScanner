Add github token in .env

Just run following commands one by one.
```bash
python3 -m venv venv
source venv/bin/activate
python3 main.py
```
For running with Docker
```bash
docker build -t github-scanner .
docker run -e GITHUB_TOKEN="" -v $(pwd)/output:/app/output github-scanner
```