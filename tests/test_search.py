from hangeul.search import matches, search_filter


def test_chosung_matches():
    target = "서강대학교"
    assert matches(target, "ㅅㄱㄷ") is True
    assert matches(target, "ㅅㄱㄷㅎㄱ") is True
    assert matches(target, "ㅎㅇㄷ") is False


def test_jaso_matches():
    target = "한글"
    assert matches(target, "ㅎㅏㄴ") is True
    assert matches(target, "ㅎㅏㄴㄱㅡㄹ") is True
    assert matches(target, "ㅎㅡㄹ") is False


def test_search_filter():
    list_data = ["사과", "수박", "복숭아", "포도"]
    assert search_filter(list_data, "ㅅㅂ") == ["수박"]
    assert search_filter(list_data, "ㅅ") == ["사과", "수박", "복숭아"]


def test_choseong_only_converts_query():
    """choseong_only=True면 검색어도 초성으로 변환해 비교"""
    assert matches("서강대학교", "서강", choseong_only=True) is True
    assert matches("서강대학교", "소고", choseong_only=True) is True
    assert matches("서강대학교", "ㅅㄱ", choseong_only=True) is True
    assert matches("서강대학교", "강남", choseong_only=True) is False
