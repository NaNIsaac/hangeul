from hangeul.josa import attach, get_josa

def test_josa_basic():
    assert attach("사과", "이/가") == "사과가"
    assert attach("수박", "이/가") == "수박이"
    assert attach("바다", "은/는") == "바다는"
    assert attach("강", "은/는") == "강은"

def test_josa_ro_exception():
    """'로/으로'의 ㄹ 받침 예외 테스트"""
    assert attach("강", "으로/로") == "강으로"
    assert attach("물", "으로/로") == "물로"
    assert attach("길", "으로/로") == "길로"

def test_josa_number():
    """숫자 발음 기반 조사 테스트"""
    assert attach("1", "이/가") == "1이"   # 일-이
    assert attach("2", "이/가") == "2가"   # 이-가
    assert attach("3", "은/는") == "3은"   # 삼-은
    assert attach("7", "로/으로") == "7로" # 칠-로 (ㄹ받침)
    assert attach("8", "로/으로") == "8로" # 팔-로 (ㄹ받침)
    assert attach("10", "을/를") == "10을" # 십-을

def test_josa_alphabet_acronym():
    """영문 대문자 약어 테스트"""
    assert attach("IBM", "이/가") == "IBM이" # 아이비엠(ㅁ받침)
    assert attach("AI", "이/가") == "AI가"   # 에이아이(받침없음)
    assert attach("SDK", "은/는") == "SDK는" # 에스디케이(받침없음)
    assert attach("SQL", "로/으로") == "SQL로" # 에스큐엘(ㄹ받침)

def test_josa_parentheses():
    """괄호 처리 테스트"""
    assert attach("애플(Apple)", "이/가") == "애플(Apple)이"
    assert attach("삼성(Samsung)", "은/는") == "삼성(Samsung)은"