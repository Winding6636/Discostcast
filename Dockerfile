FROM python:3.10.11-alpine
LABEL maintainer="Winding"

# Add project source
WORKDIR /musicbot
COPY . ./
# Const_pkg
RUN apk update \
&& apk add --no-cache \
  ca-certificates \
  ffmpeg \
  opus-dev \
  python3 \
  libsodium-dev \
  bash \
  git \
  wget \
  curl \
  patch \
\
# Build-deps_pkg
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
# nndownloadインスヨール
#RUN git clone -b v1.11 https://github.com/AlexAplin/nndownload.git /tmp/nndownload \
#    && pip install -r /tmp/nndownload/requirements.txt \
#    && pip install /tmp/nndownload && rm -rf /tmp/nndownload
ADD config /usr/src/musicbot/config
ADD .netrc /root/.netrc
RUN chmod og-rw /root/.netrc

# Patchs
#ADD ./env/ytdl_patch.sh /usr/src/musicbot
RUN sh ./env/ytdl_patch.sh
#RUN wget https://raw.githubusercontent.com/Winding6636/DiscoMusicBot/patch/ytdl.patch && patch -p1 < ytdl.patch

#Cleanup
RUN apk del .build-deps

# 構成をマッピングするためのボリュームを作成します
VOLUME ["/musicbot/audio_cache", "/musicbot/config", "/musicbot/data", "/musicbot/logs"]
ENV APP_ENV=docker
ENTRYPOINT ["/bin/sh", "docker-entrypoint.sh"]
