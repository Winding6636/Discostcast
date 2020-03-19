import os
import sys
import asyncio
import concurrent.futures
import nndownload
import time

def downloader(song_url, output_path, quality):
    try:
        #nndownload.execute("-g", "-n", "-m", "-vq", "low", "-aq", "archive_aac_192kbps", "-l", "--thread", "8", "-o", output_path, song_url)
        #nndownload.execute("-q", "-g", "-n", "-vq", quality, "-aq", "archive_aac_192kbps",  "--thread", "8", "-o", output_path, song_url)
        nndownload.execute("-q", "-g", "-n", "-aq", "archive_aac_192kbps",  "--thread", "8", "-o", output_path, song_url)
    except (nndownload.nndownload.FormatNotAvailableException, nndownload.nndownload.ParameterExtractionException) as e:
        try:
            time.sleep(1)
            nndownload.execute("-q", "-g", "-n", "-aq", "archive_aac_64kbps", "--thread", "8", "-o", output_path, song_url)
        except:
            print("[downloader] : safe")
            nndownload.execute("-q", "-g", "-n", "--thread", "10", "-o", output_path, song_url)
    except ZeroDivisionError as e:
        print("Donwload Failed : ", e.args)

def safe_downloader(song_url, output_path, quality):
    try:
        #nndownload.execute("-g", "-n", "-m", "-vq", "low", "-aq", "archive_aac_192kbps", "-l", "--thread", "8", "-o", output_path, song_url)
        nndownload.execute("-q", "-g", "-aq", "archive_aac_192kbps",  "--thread", "8", "-o", output_path, song_url)
    except (nndownload.nndownload.FormatNotAvailableException, nndownload.nndownload.ParameterExtractionException) as e:
        try:
            time.sleep(1)
            nndownload.execute("-q", "-g", "-vq", quality, "-aq", "archive_aac_64kbps", "--thread", "8", "-o", output_path, song_url)
        except:
            print("[downloader] : safe")
            nndownload.execute("-q", "-g", "--thread", "10", "-o", output_path, song_url)
    except ZeroDivisionError as e:
        print("Donwload Failed : ", e.args)

async def select(loop, song_url, output_path):
    #for quality in [ "archive_h264_200kbps_360p", "archive_h264_360p", "archive_h264_360p_low", "archive_h264_300kbps_360p", "archive_h264_600kbps_360p" ]:
    #for quality in [ "archive_h264_360p_low", "archive_h264_360p", "archive_h264_200kbps_360p", "archive_h264_300kbps_360p", "archive_h264_600kbps_360p" ]:
    for quality in [ "archive_h264_300kbps_360p", "archive_h264_600kbps_360p", "archive_h264_1600kbps_540p", ]:
        try:
            downloader(song_url, output_path, quality)
            result = True
            break
        except:
            try:
                print("[downloader] : .netrc nicovideo.jp notfound.")
                safe_downloader(song_url, output_path, quality)
                break
            except:
                pass
    else:
        result = False


if __name__ == "__main__":
    #print('sys.argv: ', sys.argv)
    #print('sys.argv[1]: ', sys.argv[1])
    #print('sys.argv[2]: ', sys.argv[2])
    loop = asyncio.get_event_loop()
    print("[nicomodule] : run:main")
    loop.run_until_complete(select(loop, sys.argv[1], sys.argv[2]))
    print("[nicomodule] : end:main")