import sys
import asyncio
import nndownload
import logging

async def download(loop, session, song_url, output_path):
    try:
        if session:
            nndownload.execute("--session-cookie", session, "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest" )
        else:
            #nndownload.execute("-n", "-g", "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest", "-aq", "highest")
            nndownload.execute("-n", "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest" )
    except:
        try:
            if session:
                nndownload.execute("--session-cookie", session, "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest" )    
            else:
                nndownload.execute("-n", "-q", "-o", output_path, song_url, "-r 20", "-vq", "lowest" )
        except:
            exit (1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(loop, sys.argv[1], sys.argv[2], sys.argv[3]))