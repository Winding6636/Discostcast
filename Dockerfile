FROM python:3.10.11-alpine
LABEL maintainer="Winding"

WORKDIR /musicbot
COPY . ./

# Install runtime deps + build-time deps (virtual group for cleanup)
RUN apk update \
  && apk add --no-cache \
    ca-certificates \
    ffmpeg \
    opus-dev \
    libffi \
    libsodium \
    bash \
    git \
    wget \
    curl \
    patch \
    nodejs \
  && apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    libc-dev \
    libffi-dev \
    make \
    musl-dev \
    python3-dev

#Scripts
WORKDIR /musicbot
#RUN  git clone -b modified https://github.com/Winding6636/DiscoMusicBot.git /musicbot \
#&&git pull --tags
# pip依存関係をインストールする
RUN pip3 install --upgrade pip \
  && pip3 install --no-cache-dir -r requirements.txt
ADD config /musicbot/config
ADD .netrc /root/.netrc
RUN chmod og-rw /root/.netrc

# Patchs
#ADD ./env/ytdl_patch.sh /musicbot
#RUN sh ./env/ytdl_patch.sh
#RUN wget https://raw.githubusercontent.com/Winding6636/DiscoMusicBot/patch/ytdl.patch && patch -p1 < ytdl.patch

#Cleanup
RUN apk del .build-deps

VOLUME ["/musicbot/audio_cache", "/musicbot/config", "/musicbot/data", "/musicbot/logs"]
ENV APP_ENV=docker
ENTRYPOINT ["/bin/sh", "docker-entrypoint.sh"]
