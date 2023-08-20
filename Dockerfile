FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y chromium libglib2.0 libnss3 libgconf-2-4 libfontconfig1 gnupg wget curl cron unzip jq && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

RUN CHROME_URL=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chrome[] | select(.platform == "linux64") | .url') && \
    curl -sSLf --retry 3 --output /tmp/chrome-linux64.zip "$CHROME_URL" && \
    unzip /tmp/chrome-linux64.zip -d /opt && \
    ln -s /opt/chrome-linux64/chrome /usr/local/bin/chrome && \
    rm /tmp/chrome-linux64.zip

RUN CHROMEDRIVER_URL=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform == "linux64") | .url') && \
    curl -sSLf --retry 3 --output /tmp/chromedriver-linux64.zip "$CHROMEDRIVER_URL" && \
    unzip -o /tmp/chromedriver-linux64.zip -d /tmp && \
    rm -rf /tmp/chromedriver-linux64.zip && \
    mv -f /tmp/chromedriver-linux64/chromedriver "/usr/local/bin/chromedriver" && \
    chmod +x "/usr/local/bin/chromedriver"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt --no-cache-dir
RUN touch /app/cron.log && chmod 666 /app/cron.log
RUN chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]
