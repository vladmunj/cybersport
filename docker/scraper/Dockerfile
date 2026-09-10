FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo Etc/UTC > /etc/timezone
ENV TZ=Etc/UTC
COPY app ./app
COPY services ./services
COPY exceptions ./exceptions
COPY scripts ./scripts
RUN chmod +x ./scripts/*