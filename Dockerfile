FROM python:3.10-alpine3.20
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
  && apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    libc-dev \
    libffi-dev \
    make \
    musl-dev \
    python3-dev

# yt-dlp requires deno >= 2.3.0 to solve YouTube's JS challenges (EJS).
# Alpine 3.20's own deno package (1.43.5) is too old. Pull a newer, version-pinned
# deno plus its newer shared-lib deps from edge, WITHOUT adding edge to
# /etc/apk/repositories permanently -- that previously caused apk to pull
# unrelated packages (e.g. bash) from edge too and broke the image.
RUN apk add --no-cache \
    --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main \
    --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community \
    'deno=2.7.4-r2' \
    'libssl3=3.5.7-r0' \
    'libcrypto3=3.5.7-r0' \
    'sqlite-libs=3.53.4-r0' \
    'icu-libs=78.1-r0'

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
