from hangeul.core import assemble, disassemble, qwerty2han


def test_qwerty2han():
    assert qwerty2han("gksrmf") == "ㅎㅏㄴㄱㅡㄹ"
    assert qwerty2han("R r") == "ㄲ ㄱ"
    assert qwerty2han("123!@#") == "123!@#"


def test_assemble_basic():
    assert assemble("ㄱㅏ") == "가"
    assert assemble("ㄱㅏㄴ") == "간"
    assert assemble("ㄱㅏㅂㅅ") == "값"
    assert assemble("ㅗㅏ") == "ㅘ"


def test_assemble_liaison():
    """연음 법칙 및 겹받침 분리 테스트"""
    assert assemble("ㄱㅏㅂㅅㅇㅣ") == "값이"
    assert assemble("ㄱㅏㅂㅅㅣ") == "갑시"
    assert assemble("ㅇㅏㄴㅈㅇㅏ") == "앉아"
    assert assemble("ㅇㅗㅐㅇㅏㄴㄷㅗㅣ") == "왜안되"


def test_disassemble():
    assert disassemble("한글") == "ㅎㅏㄴㄱㅡㄹ"
    assert disassemble("값") == "ㄱㅏㅂㅅ"
    assert disassemble("과") == "ㄱㅗㅏ"
    assert disassemble("왜") == "ㅇㅗㅐ"


def test_round_trip():
    """조합 후 분해했을 때 원본과 동일한지 확인"""
    targets = ["한글", "값이", "앉아", "도전", "학교"]
    for t in targets:
        assert assemble(disassemble(t)) == t


def test_assemble_lone_vowel_then_consonant():
    """초성 없는 모음 뒤의 자음은 앞 모음과 합쳐지지 않아야 함"""
    assert assemble("ㅏㄱ") == "ㅏㄱ"
    assert assemble("ㅗㄱㅏ") == "ㅗ가"
    assert assemble("ㅏㄳ") == "ㅏㄳ"
