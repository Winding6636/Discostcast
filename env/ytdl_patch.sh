#!/bin/sh
##  YoutubeDL Patch Script PiP
##      Winding_feat.NKTN
##
##  youtube fuck 429 patch , niconico sm video_id patch, ytsearch patch

# 準備
echo :-: Modified Patch Prov :-:
mkdir -p patch && cd patch
pip download --no-binary :all: youtube-dl
mkdir youtube-dl && tar --strip-components 1 -xf youtube_dl-*.tar.gz  -C youtube-dl
git clone https://gitlab.com/colethedj/youtube-dl-429-patch.git
git clone https://github.com/Winding6636/DiscoMusicBot.git musicbot
cd musicbot && git checkout patch && cd ../
# パッチ
echo :-: Patch RUN :-:
cd youtube-dl
sed -i -e '$a __version__ = __version__ + " modified:"' ./youtube_dl/version.py
patch -t -p1 < ../youtube-dl-429-patch/youtube_dl_429.patch
result=0
output=$(python youtube_dl/__main__.py --youtube-bypass-429 -s SiSV9SgUbj0 --wget-limit-rate 102400) || result=$?
if [ ! "$result" = "0" ]; then
    echo >&2 '[PatchProcess] ERROR: Youtube-DL youtube-429 patch is not correct.'
else
    echo Youtube-429-Too-Many-Requests Patch.
    sed -i -e '$a __version__ = __version__ + " _429-patch"' ./youtube_dl/version.py
fi
patch -t -p1 < ../musicbot/niconico_sm.patch
result=0
output=$(python youtube_dl/__main__.py sm33203699 -s) || result=$?
if [ ! "$result" = "0" ]; then
    echo >&2 '[PatchProcess] ERROR: Youtube-DL nicovideo.jp sm,nm,so patch is not correct.'
else
    echo niconico sm patch.
    sed -i -e '$a __version__ = __version__ + ", _nicosm-patch"\n' ./youtube_dl/version.py
fi
patch -t -p1 < ../musicbot/ytdl_searchjson.patch
result=0
output=$(python youtube_dl/__main__.py ytsearch:とにほん -s) || result=$?
if [ ! "$result" = "0" ]; then
    echo >&2 '[PatchProcess] ERROR: Youtube-DL ytsearch json fix patch.'
else
    echo Youtube-ytsearch-json Patch.
    sed -i -e '$a __version__ = __version__ + ", _ytsearch-patch"\n' ./youtube_dl/version.py
fi

pip install .
cd ../../
rm -rf patch