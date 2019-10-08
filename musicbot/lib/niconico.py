import os
import sys
import asyncio
import concurrent.futures
import nndownload

def nndl(song_url,output_path):
    try:
        nndownload.execute("-g", "-q", "--thread", "8", "-o", output_path, song_url)
    except Exception as e:
        raise ExtractionError(e)
        print("Donwload Failed.")

async def ncdl(loop):
    try:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, nndl(url,output_path))
            print('custom thread pool')
    finally:
        print("DLProcessEND")

if __name__ == "__main__":
    #print('sys.argv: ', sys.argv)
    #print('sys.argv[1]: ', sys.argv[1])
    #print('sys.argv[2]: ', sys.argv[2])
    loop = asyncio.get_event_loop()
    try:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = loop.run_in_executor(pool, nndl(sys.argv[1],sys.argv[2]))
    finally:
        print("[nicomodule] : end:main")
