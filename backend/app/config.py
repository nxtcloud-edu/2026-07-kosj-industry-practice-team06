"""환경변수 설정 모듈"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 탐색 (backend/.env → 프로젝트 루트/.env)
env_path = Path(__file__).parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATA_API_KEY = os.getenv("DATA_API_KEY", "")

# 조치원 기준 좌표
DEFAULT_LAT = 36.604561
DEFAULT_LNG = 127.298342

# SQLite DB 경로
DATABASE_PATH = Path(__file__).parent.parent / "store.db"
