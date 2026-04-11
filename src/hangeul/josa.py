import re
from types import MappingProxyType
from typing import Final

# 1. 상수 정의
_JOSA_MAP: Final = MappingProxyType({
    "이/가": ("가", "이"),
    "은/는": ("는", "은"),
    "을/를": ("를", "을"),
    "와/과": ("와", "과"),
    "아/야": ("야", "아"),
    "나/이나": ("나", "이나"),
    "란/이란": ("란", "이란"),
    "랑/이랑": ("랑", "이랑"),
    "라/이라": ("라", "이라"),
    "예요/이에요": ("예요", "이에요"),
})

# 로 계열 조사는 'ㄹ' 받침 예외 규칙을 동일하게 공유함
_RO_JOSAS: Final[tuple[str, ...]] = ("로/으로", "로서/으로서", "로써/으로써", "로부터/으로부터")

# 영문 알파벳 끝글자 발음 데이터 (약어 처리용)
_ALPHABET_BATTCHIM: MappingProxyType = MappingProxyType({
    'A': '에이', 'B': '비', 'C': '씨', 'D': '디', 'E': '이',
    'F': '에프', 'G': '지', 'H': '에이치', 'I': '아이', 'J': '제이',
    'K': '케이', 'L': '엘', 'M': '엠', 'N': '엔', 'O': '오',
    'P': '피', 'Q': '큐', 'R': '알', 'S': '에스', 'T': '티',
    'U': '유', 'V': '브이', 'W': '더블유', 'X': '엑스', 'Y': '와이', 'Z': '제트'
})

def _get_jong_idx(char: str) -> int:
    """한글 음절의 종성 인덱스를 반환합니다."""
    if '가' <= char <= '힣':
        return (ord(char) - 0xAC00) % 28
    return -1

def _analyze_last_char(word: str) -> tuple[bool, int]:
    """
    단어의 마지막 글자를 분석하여 (받침_여부, 종성_인덱스)를 반환합니다.
    괄호, 숫자, 영문 약어 처리를 포함합니다.
    """
    if not word:
        return False, -1

    # 1. 괄호 제거: "단어(Content)" -> "단어" 추출
    base_word = re.sub(r'\(.*\)$', '', word).strip()
    if not base_word:
        base_word = word
    last = base_word[-1]

    # 2. 한글 분석
    if '가' <= last <= '힣':
        idx = _get_jong_idx(last)
        return idx > 0, idx

    # 3. 숫자 분석 (0, 1, 3, 6, 7, 8 은 받침 있음 / 1, 7, 8 은 'ㄹ' 계열)
    if last.isdigit():
        has_bat = last in "013678"
        return has_bat, (8 if last in "178" else (1 if has_bat else 0))

    # 4. 영문 대문자 약어 분석 (예: SDK, AI, SQL)
    if base_word.isupper() and 'A' <= last <= 'Z':
        pronunciation = _ALPHABET_BATTCHIM.get(last, "")
        if pronunciation:
            idx = _get_jong_idx(pronunciation[-1])
            return idx > 0, idx

    # 5. 기타 (일반 영문 단어, 특수문자 등)는 받침 없음으로 간주
    return False, 0

def get_josa(word: str, pattern: str) -> str:
    """
    단어와 조사 패턴을 분석하여 적절한 조사를 선택합니다.
    """
    if not word:
        return ""

    has_bat, jong_idx = _analyze_last_char(word)
    norm_pattern = "/".join(sorted(pattern.split("/")))

    match norm_pattern:
        # '로' 계열 특수 처리 (받침이 없거나 'ㄹ' 받침인 경우 '로')
        case p if p in _RO_JOSAS:
            parts = pattern.split('/') # 사용자 입력 순서 유지
            # 보통 (로/으로) 또는 (으로/로) 순서임
            ro, euro = (parts[0], parts[1]) if len(parts[0]) < len(parts[1]) else (parts[1], parts[0])
            return ro if not has_bat or jong_idx == 8 else euro

        # 일반 조사 처리
        case p if p in _JOSA_MAP:
            vowel_case, consonant_case = _JOSA_MAP[p]
            return consonant_case if has_bat else vowel_case

        # 맵에 없는 패턴은 (받침있음/받침없음) 순서로 가정하여 처리
        case _:
            parts = pattern.split('/')
            if len(parts) != 2:
                raise ValueError(f"지원하지 않는 조사 패턴입니다: {pattern}")
            return parts[0] if has_bat else parts[1]

def attach(word: str, pattern: str) -> str:
    """단어에 조사를 결합합니다."""
    return f"{word}{get_josa(word, pattern)}"