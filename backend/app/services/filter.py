"""금지어 필터링 서비스 (허위·과장 광고 방지)"""

PROHIBITED_WORDS = [
    "전국 1위", "최고", "최저가", "업계 최초",
    "무조건", "100% 보장", "기적", "1등",
    "독보적", "압도적", "완벽한", "유일한",
]


def check_prohibited_words(text: str) -> str:
    """금지어가 포함된 경우 해당 단어를 제거합니다."""
    filtered = text
    for word in PROHIBITED_WORDS:
        if word in filtered:
            filtered = filtered.replace(word, "")
    return filtered
