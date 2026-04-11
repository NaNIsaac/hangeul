from .core import disassemble

def _levenshtein_distance(s1: str, s2: str) -> int:
    """두 문자열 간의 편집 거리(Levenshtein Distance)를 계산합니다."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)

    if not s2:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def jamo_similarity(str1: str, str2: str) -> float:
    """
    두 문자열을 자소 단위로 분해하여 유사도(0.0 ~ 1.0)를 측정합니다.
    1.0에 가까울수록 두 문자열이 유사함을 의미합니다.
    """
    if str1 == str2:
        return 1.0
    
    # 자소 단위로 완전히 분해 (예: '값' -> 'ㄱㅏㅂㅅ')
    s1_dis = disassemble(str1)
    s2_dis = disassemble(str2)
    
    if not s1_dis or not s2_dis:
        return 0.0
    
    distance = _levenshtein_distance(s1_dis, s2_dis)
    max_len = max(len(s1_dis), len(s2_dis))
    
    # 유사도 계산 공식: 1 - (거리 / 최대 길이)
    return 1.0 - (distance / max_len)