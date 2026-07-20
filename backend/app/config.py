"""환경변수 설정 모듈"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATA_API_KEY = os.getenv("DATA_API_KEY", "")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY", "")
