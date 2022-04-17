import os

baseDir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(baseDir, "temp")
if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

PORT = "8887"

LOG_PATH = os.path.join(baseDir, "logs")
if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)