"""환경변수 설정 모듈"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 탐색: backend/.env → 프로젝트 루트/.env
_backend_dir = Path(__file__).parent.parent
_root_dir = _backend_dir.parent

if (_backend_dir / ".env").exists():
    load_dotenv(_backend_dir / ".env")
elif (_root_dir / ".env").exists():
    load_dotenv(_root_dir / ".env")
else:
    load_dotenv()  # 기본 탐색

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATA_API_KEY = os.getenv("DATA_API_KEY", "")

# 조치원 기준 좌표
DEFAULT_LAT = 36.604561
DEFAULT_LNG = 127.298342

# SQLite DB 경로
DATABASE_PATH = Path(__file__).parent.parent / "store.db"
