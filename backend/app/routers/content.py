"""콘텐츠 생성 API 라우터"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm import generate_marketing_content

router = APIRouter()


class ContentRequest(BaseModel):
    prompt: str  # 사장님의 자연어 입력
    store_name: str = ""  # 가게명 (선택)
    location: str = "조치원"  # 위치


class ContentResponse(BaseModel):
    success: bool
    instagram_caption: str = ""
    banner_text: str = ""
    error: str = ""


@router.post("/generate", response_model=ContentResponse)
async def generate_content(req: ContentRequest):
    """자연어 입력을 받아 마케팅 콘텐츠를 생성합니다."""
    try:
        result = generate_marketing_content(req.prompt, req.location)
        return ContentResponse(
            success=True,
            instagram_caption=result.get("instagram", ""),
            banner_text=result.get("banner", ""),
        )
    except Exception as e:
        return ContentResponse(success=False, error=str(e))
