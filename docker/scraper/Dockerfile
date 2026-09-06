FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY scraper ./scraper
COPY services ./services
COPY exceptions ./exceptions
COPY scripts ./scripts
RUN chmod +x ./scripts/*