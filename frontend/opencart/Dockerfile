FROM python:3.13-slim

USER root

RUN apt-get update && apt-get install -y \
    chromium \
    firefox-esr \
    xvfb \
    x11-utils \
    libgl1-mesa-dri \
    libglx-mesa0 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/auotests
COPY . /root/auotests/

RUN pip install -U pip
RUN pip install -r requirements.txt

ENV DISPLAY=:99 \
    ELECTRON_DISABLE_SANDBOX=1 \
    CHROME_BIN=/usr/bin/chromium \
    XVFB_WHD=1920x1080x24+32

ENTRYPOINT ["sh", "/root/auotests/entrypoint.sh"]