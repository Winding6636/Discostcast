#!/bin/sh
##  YoutubeDL Patch Script PiP
##      Winding_feat.T@9N
##
##  youtube fuck 429 patch , niconico sm video_id patch, ytsearch patch

# 準備
echo :-: Modified Patch Prov Run :-:
mkdir -p patch && cd patch
#pip download --no-binary :all: youtube-dl
pip download --no-binary :all: yt-dlp
#mkdir youtube-dl && tar --strip-components 1 -xf youtube_dl-*.tar.gz  -C youtube-dl
mkdir yt-dlp && tar --strip-components 1 -xf yt-dlp-*.tar.gz  -C yt-dlp
git clone https://gitlab.com/colethedj/youtube-dl-429-patch.git
git clone -b patch https://github.com/Winding6636/DiscoMusicBot.git patchfile
# パッチ
echo :-: MusicBot Change DLoader youtube_dl to yt-dlp :-:
cd ..
patch -R -t -p1 < patch/patchfile/ytdl.patch
cd patch

echo :-: Patch yt-dlp :-:
cd ./yt-dlp
sed -i -e '$a __version__ = __version__ + ".modified"' ./yt_dlp/version.py
patch -t -p1 < ../patchfile/ytdlp_nicosm.patch
python devscripts/make_lazy_extractors.py
result=0
output=$(python yt_dlp/__main__.py sm33203699 -s) || result=$?
if [ ! "$result" = "0" ]; then
    echo >&2 '[PatchProcess] ERROR: yt-dlp nicovideo.jp sm,nm,so patch is not correct.'
    exit 1
else
    echo  :: Niconico VideoId shortPatch.
    sed -i -e '$a __version__ = __version__ + ".nicoIDshort"\n' ./yt_dlp/version.py
fi
pip install .

cd ../../
rm -rf patch
exit 0