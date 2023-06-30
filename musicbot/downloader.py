import os
import asyncio
import logging
import functools
#import youtube_dl
import yt_dlp as youtube_dl
import subprocess, re, time
import json

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from .config import Config, ConfigDefaults
from .lib import niconico

log = logging.getLogger(__name__)

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "usenetrc": True,
    "extract-audio": True,
    "audio-quality": 0,
    "youtube-bypass-429": True,
    "--youtube-bypass-429": True,
    "wget-limit-rate": "8191",
    "--rm-cache-dir": True,
    "rm-cache-dir": True
}

# Fuck your useless bugreports message that gets two link embeds and confuses users
youtube_dl.utils.bug_reports_message = lambda: ""

"""
    Alright, here's the problem.  To catch youtube-dl errors for their useful information, I have to
    catch the exceptions with `ignoreerrors` off.  To not break when ytdl hits a dumb video
    (rental videos, etc), I have to have `ignoreerrors` on.  I can change these whenever, but with async
    that's bad.  So I need multiple ytdl objects.

"""


class Downloader:
    def __init__(self, download_folder=None):
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        #self.unsafe_ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        #self.safe_ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        #self.safe_ytdl.params["ignoreerrors"] = True
        self.download_folder = download_folder

        if download_folder:
            # print("setting template to " + os.path.join(download_folder, otmpl))
            otmpl = ytdl_format_options["outtmpl"]
            ytdl_format_options["outtmpl"] = os.path.join(download_folder, json.dumps(otmpl))

        self.unsafe_ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        self.safe_ytdl = youtube_dl.YoutubeDL( {**ytdl_format_options, "ignoreerrors": True} )


    @property
    def ytdl(self):
        return self.safe_ytdl

    async def extract_info(self, loop, *args, on_error=None, retry_on_error=False, **kwargs):
        """
        Runs ytdl.extract_info within the threadpool. Returns a future that will fire when it's done.
        If `on_error` is passed and an exception is raised, the exception will be caught and passed to
        on_error as an argument.
        """
        if callable(on_error):
            try:
                return await loop.run_in_executor(self.thread_pool, functools.partial(self.unsafe_ytdl.extract_info, *args, **kwargs))

            except Exception as e:

                # (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError)
                # I hope I don't have to deal with ContentTooShortError's
                if asyncio.iscoroutinefunction(on_error):
                    asyncio.ensure_future(on_error(e), loop=loop)

                elif asyncio.iscoroutine(on_error):
                    asyncio.ensure_future(on_error, loop=loop)

                else:
                    loop.call_soon_threadsafe(on_error, e)

                if retry_on_error:
                    return await self.safe_extract_info(loop, *args, **kwargs)
        else:
            return await loop.run_in_executor(self.thread_pool, functools.partial(self.unsafe_ytdl.extract_info, *args, **kwargs))

    async def safe_extract_info(self, loop, *args, **kwargs):
        return await loop.run_in_executor(self.thread_pool, functools.partial(self.safe_ytdl.extract_info, *args, **kwargs))


    async def nico_extract(self, loop, config, song_url, output_path):
        #save_path = "" + self.download_folder + "/{id}.mp4"
        id = re.search(r'(sm|nm|so)[0-9]+',output_path)
        if id != None:
            save_path = "audio_cache/" + id.group() + ".mp4"
        else:
            id = re.search(r'[0-9]+',output_path)
            save_path = "audio_cache/" + id.group() + ".mp4"
        
        log.everything("#[PATH]# : %s",song_url)
        log.everything("#[PATH]# : %s",save_path)
        log.everything("#[PATH]# : %s",output_path)
        #log.debug("#[PATH]# : %s",rename_path)

        def filechkpass():
            log.debug("FileExistenceCheck")
            try:
                os.path.isfile(save_path)
            except ZeroDivisionError:
                os.remove(save_path)

        def get_run():
            retime = [ 20, 30, 120, 240, 320 ]
            for _ in retime:
                try:
                    subprocess.call(["python", "./musicbot/lib/niconico.py", config.niconico_session, song_url, save_path],timeout=_)
                    break
                except subprocess.TimeoutExpired as e:
                    filechkpass()
                    log.debug("[DownloadProcess] : Timeout. - " + str(_) + "s - Retry...")
                    time.sleep(3)
                except:
                    filechkpass()
                    log.debug("[DownloadProcess] :  Download Error...")
                    time.sleep(3)

        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, functools.partial(get_run))
        
        try:
            os.path.isfile(save_path)
            try:
                os.rename(save_path,output_path)
            except:
                pass
        except Exception as e:
            log.error("[DownloadProcess] :  Download Error... ― ダウンロードに失敗しました。")
            result = False
        else:
            result = True

        return  output_path
        