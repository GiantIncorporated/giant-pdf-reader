import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME=os.environ.get("APP_NAME")
ORG_NAME=os.environ.get("ORG_NAME")
DEV_MODE=os.environ.get("DEV_MODE")
DEV_SERVER_URL=os.environ.get("DEV_SERVER_URL")
DEVELOPMENT=os.environ.get("DEVELOPMENT")
QTWEBENGINE_REMOTE_DEBUGGING=os.environ.get("QTWEBENGINE_REMOTE_DEBUGGING", "9222")

os.environ.setdefault("QTWEBENGINE_REMOTE_DEBUGGING", QTWEBENGINE_REMOTE_DEBUGGING)

PRODUCTION_PATH= os.path.join(os.path.dirname(__file__), "frontend", "dist", "index.html")

PACKAGE_ROOT = Path(__file__).resolve().parent

