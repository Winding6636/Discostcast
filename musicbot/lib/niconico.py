import os
import sys
import asyncio
import concurrent.futures
import nndownload
import time

def downloader(song_url, output_path, quality):
    try:
        #nndownload.execute("-g", "-n", "-m", "-vq", "low", "-aq", "archive_aac_192kbps", "-l", "--thread", "8", "-o", output_path, song_url)
        nndownload.execute("-g", "-n", "-vq", quality, "-aq", "archive_aac_192kbps",  "--thread", "10", "-o", output_path, song_url)
    except nndownload.nndownload.FormatNotAvailableException as e:
        try:
            time.sleep(1)
            nndownload.execute("-g", "-n", "-vq", quality, "-aq", "archive_aac_64kbps", "--thread", "10", "-o", output_path, song_url)
        except:
            time.sleep(1)
            nndownload.execute("-g", "-n", "-vq", quality,  "--thread", "10", "-o", output_path, song_url)
    except ZeroDivisionError as e:
        print("Donwload Failed : ", e.args)

async def select(loop, song_url, output_path):
    try:
        downloader(song_url, output_path, 'archive_h264_360p')
    except:
        try:
            time.sleep(2)
            downloader(song_url, output_path, 'archive_h264_360p_low')
        except:
            try:
                time.sleep(2)
                downloader(song_url, output_path, 'archive_h264_200kbps_360p')
            except:
                try:
                    time.sleep(2)
                    downloader(song_url, output_path, 'archive_h264_300kbps_360p')
                except:
                    time.sleep(2)
                    downloader(song_url, output_path, None)

if __name__ == "__main__":
    #print('sys.argv: ', sys.argv)
    #print('sys.argv[1]: ', sys.argv[1])
    #print('sys.argv[2]: ', sys.argv[2])
    loop = asyncio.get_event_loop()
    print("[nicomodule] : run:main")
    loop.run_until_complete(select(loop, sys.argv[1], sys.argv[2]))
    print("[nicomodule] : end:main")