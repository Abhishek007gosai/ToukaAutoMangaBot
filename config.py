# Made by @codexnano from scratch.
# If you find any bugs, please let us know in the channel updates.
# You can 'git pull' to stay updated with the latest changes.

import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    API_ID = 23537462
    API_HASH = "c9599a5aa61ee8ca4f5e778d20c61f24"
    BOT_TOKEN = "7686806902:AAGxlvsZGrOHCXPbS6qV3X_hJzr7VlrzwC8"
    MONGO_DB_URI = "mongodb+srv://hanxsooyoung:qGsVMuuKjE12Gewz@cluster0.oooqdg5.mongodb.net/"
    OWNER_ID = [int(x) for x in os.getenv("OWNER_ID", "8226767954").split()] if os.getenv("OWNER_ID") else []
    LOG_GROUP = -1002456565415
    MAX_IMAGE_SIZE = 10 * 1024 * 1024
    MAX_PDF_SIZE = 50 * 1024 * 1024
    DOWNLOAD_DIR = "downloads"
    MAX_IMAGE_WIDTH = 2500
    JPEG_QUALITY = 100
    ENABLE_WEBP = True # Option to use webp if needed
    FSUB_CHANNELS = []
    _fsub = os.getenv("FSUB_CHANNELS", "")
    if _fsub:
        for x in _fsub.split():
            try:
                FSUB_CHANNELS.append(int(x))
            except ValueError:
                FSUB_CHANNELS.append(x)
