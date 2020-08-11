#!/bin/sh
##  YoutubeDL Patch Script PiP
##      Winding_feat.NKTN
##
##  youtube fuck 429 patch , niconico sm video_id patch

mkdir patch && cd patch
pip download --no-binary :all: youtube-dl
mkdir youtube-dl && tar --strip-components 1 -xf youtube_dl-*.tar.gz  -C youtube-dl
git clone https://gitlab.com/colethedj/youtube-dl-429-patch.git
wget -q -O ./niconico_sm.patch https://raw.githubusercontent.com/Winding6636/youtube-dl/nico_short/niconico_sm.patch
cd youtube-dl
git apply ../youtube-dl-429-patch/youtube_dl_429.patch
patch -p1 -d . < ../niconico_sm.patch
sed -i -e '$a __version__ = __version__ + " modified: _429-patch"' ./youtube_dl/version.py
sed -i -e '$a __version__ = __version__ + ", _nicosm-patch"\n' ./youtube_dl/version.py
pip install .
cd ../../
rm -rf patch