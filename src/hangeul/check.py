import unicodedata
from typing import Literal

from .constants import 초성, 중성, 종성

_NormalizationForm = Literal["NFC", "NFD", "NFKC", "NFKD", "nfc", "nfd", "nfkc", "nfkd"]


def normalize(text: str, form: _NormalizationForm = "NFC") -> str:
    """
    텍스트를 유니코드 정규화 형식으로 변환합니다.
    기본값은 NFC(완성형)이며, macOS 환경과의 호환성을 위해 사용합니다.
    """
    return unicodedata.normalize(form.upper(), text)


def is_han(text: str, allow_space: bool = True, allow_punctuation: bool = False) -> bool:
    if not isinstance(text, str) or not text:
        return False

    for char in text:
        if "가" <= char <= "힣" or "ㄱ" <= char <= "ㅣ":
            continue
        if allow_space and char.isspace():
            continue
        if allow_punctuation and unicodedata.category(char).startswith("P"):
            continue

        return False

    return True


def is_pure_han(text: str) -> bool:
    if not text:
        return False

    return all("가" <= c <= "힣" or "ㄱ" <= c <= "ㅣ" for c in text)


def can_cho(char: str) -> bool:
    return char in 초성


def can_jung(char: str) -> bool:
    return char in 중성


def can_jong(char: str) -> bool:
    return char in 종성


def has_batchim(char: str) -> bool:
    if len(char) != 1 or not ("가" <= char <= "힣"):
        return False
    return (ord(char) - 0xAC00) % 28 > 0
