import sys
import asyncio
import nndownload

async def download(loop, song_url, output_path):
    try:
        nndownload.execute("-n", "-g", "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest", "-aq", "highest")
    except:
        try:
            nndownload.execute("-n", "-g", "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest", "-aq", "highest")
        except:
            exit (1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(loop, sys.argv[1], sys.argv[2]))