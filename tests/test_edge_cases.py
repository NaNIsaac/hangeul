"""공개 API의 경계 조건 테스트 (빈 문자열, 비한글, 혼합 텍스트, 호환 자모)."""

import importlib.metadata

import pytest

import hangeul as han


def test_version_matches_metadata():
    assert han.__version__ == importlib.metadata.version("hangeul")


def test_all_exports_resolve():
    for name in han.__all__:
        assert hasattr(han, name), name


@pytest.mark.parametrize("func", [han.assemble, han.disassemble, han.qwerty2han, han.get_chosung])
def test_empty_string_roundtrips(func):
    assert func("") == ""


def test_empty_inputs():
    assert han.is_han("") is False
    assert han.is_pure_han("") is False
    assert han.has_batchim("") is False
    assert han.get_josa("", "이/가") == ""
    assert han.attach("", "이/가") == ""
    assert han.matches("한글", "") is False
    assert han.search_filter([], "ㅎ") == []
    assert han.similarity("", "") == 1.0
    assert han.similarity("한글", "") == 0.0
    assert han.num2han("") == ""


def test_non_hangeul_passthrough():
    text = "abc 123 !?"
    assert han.disassemble(text) == text
    assert han.assemble(text) == text
    assert han.get_chosung(text) == text
    assert han.is_han(text) is False


def test_mixed_text():
    assert han.disassemble("A값1") == "Aㄱㅏㅂㅅ1"
    assert han.assemble("Aㄱㅏㅂㅅ1") == "A값1"
    assert han.get_chosung("Python 한글") == "Python ㅎㄱ"
    assert han.assemble(han.disassemble("안녕, world! 값이 3개")) == "안녕, world! 값이 3개"
    assert han.matches("파이썬 Python", "ㅍㅇㅆ") is True


def test_compatibility_jamo():
    # 호환 자모(U+3131~U+3163)는 한글로 취급
    assert han.is_pure_han("ㄱㅏ") is True
    assert han.is_han("ㅘ") is True
    assert han.has_batchim("ㄱ") is False
    # 겹자모는 분해
    assert han.disassemble("ㄳ") == "ㄱㅅ"
    assert han.disassemble("ㅘ") == "ㅗㅏ"
    # 자모만 있으면 조합되지 않은 채로 남음
    assert han.assemble("ㄱㄴㄷ") == "ㄱㄴㄷ"
    assert han.assemble("ㅏㅓ") == "ㅏㅓ"


def test_hangeul_range_boundaries():
    assert han.disassemble("가") == "ㄱㅏ"
    assert han.disassemble("힣") == "ㅎㅣㅎ"
    assert han.has_batchim("힣") is True
    assert han.get_chosung("힣") == "ㅎ"


def test_assemble_non_jong_consonant_starts_new_syllable():
    # ㄸ, ㅃ, ㅉ은 받침이 될 수 없음
    assert han.assemble("ㄱㅏㄸㅏ") == "가따"
    assert han.assemble("ㅇㅣㅃㅏ") == "이빠"


def test_round_trip_all_syllables():
    syllables = "".join(chr(c) for c in range(0xAC00, 0xD7A4))
    assert han.assemble(han.disassemble(syllables)) == syllables


def test_josa_patterns():
    # 패턴 순서와 무관
    assert han.get_josa("책", "는/은") == "은"
    assert han.get_josa("책", "은/는") == "은"
    assert han.get_josa("사과", "을/를") == "를"
    assert han.get_josa("사과", "와/과") == "와"
    assert han.get_josa("책", "와/과") == "과"
    assert han.get_josa("학교", "으로서/로서") == "로서"
    assert han.get_josa("서울", "으로부터/로부터") == "로부터"
    # 소문자 영단어는 받침 없음으로 간주
    assert han.attach("apple", "이/가") == "apple가"
    # 맵에 없는 패턴은 (받침 있음/받침 없음) 순서
    assert han.get_josa("책", "이다/다") == "이다"
    assert han.get_josa("사과", "이다/다") == "다"
    with pytest.raises(ValueError):
        han.get_josa("책", "가/나/다")


def test_num2han_inputs():
    assert han.num2han("1,000") == "천"
    assert han.num2han(" 42 ") == "사십이"
    assert han.num2han(100010001) == "일억만일"
    with pytest.raises(ValueError):
        han.num2han(-1)
    with pytest.raises(ValueError):
        han.num2han("1.5")


def test_can_jamo_rejects_syllables_and_latin():
    for f in (han.can_cho, han.can_jung, han.can_jong):
        assert f("가") is False
        assert f("a") is False


def test_constants():
    assert len(han.CHOSOENG) == 19
    assert len(han.JUNGSOENG) == 21
    assert len(han.JONGSOENG) == 28
