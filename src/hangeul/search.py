from .constants import 초성
from .core import disassemble


def get_chosung(text: str) -> str:
    """
    문자열에서 초성만 추출합니다.
    한글이 아닌 문자는 그대로 유지합니다.
    """
    result = []
    for char in text:
        if "가" <= char <= "힣":
            # 초성 인덱스 계산: (유니코드 - 0xAC00) // (21 * 28)
            idx = (ord(char) - 0xAC00) // 588
            result.append(초성[idx])
        else:
            result.append(char)
    return "".join(result)


def matches(target: str, query: str, choseong_only: bool = False) -> bool:
    """
    초성 검색 및 자소 단위 검색을 수행합니다.

    Args:
        target: 검색 대상 (예: "서강대학교")
        query: 검색어 (예: "ㅅㄱㄷ" 또는 "서강")
        choseong_only: True일 경우 검색어가 초성이 아니더라도 강제로 초성 비교를 수행
    """
    if not query:
        return False

    # 검색어가 순수 초성인지 확인 (또는 강제 초성 모드)
    is_query_chosung = choseong_only or all(c in 초성 for c in query)

    if is_query_chosung:
        # 대상의 초성과 쿼리를 비교
        return get_chosung(query) in get_chosung(target)

    # 완성형/자소가 섞인 경우 자소 단위 분해 검색 (예: "ㅎㅏㄴㄱ" 검색 시 "한글" 매칭)
    return disassemble(query) in disassemble(target)


def search_filter(targets: list[str], query: str) -> list[str]:
    """
    리스트에서 검색어에 맞는 항목들을 필터링하여 반환합니다.
    """
    return [t for t in targets if matches(t, query)]
