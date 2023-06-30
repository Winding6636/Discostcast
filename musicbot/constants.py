import os.path
import subprocess

try:
  VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode("ascii").strip()
except Exception:
  VERSION = "Version_None"

AUDIO_CACHE_PATH = os.path.join(os.getcwd(), "audio_cache")
DISCORD_MSG_CHAR_LIMIT = 2000

try:
  ytdl_ver = subprocess.check_output(["yt-dlp","--version"]).decode("ascii").strip()
except Exception:
  ytdl_ver = "yt-dlp No Install"