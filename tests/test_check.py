import unicodedata

import pytest

from hangeul.check import (
    is_han, is_pure_han, has_batchim, can_cho, can_jung, can_jong, normalize
)


def test_is_pure_han():
    assert is_pure_han("가나다") is True
    assert is_pure_han("ㄱㄴㄷ") is True
    assert is_pure_han("가나12") is False
    assert is_pure_han("Hello") is False

def test_is_han_options():
    # 공백 허용 테스트
    assert is_han("가나 다", allow_space=True) is True
    assert is_han("가나 다", allow_space=False) is False
    
    # 문장 부호 허용 테스트
    assert is_han("안녕!", allow_punctuation=True) is True
    assert is_han("안녕!", allow_punctuation=False) is False
    
    # 혼합 테스트
    assert is_han("반가워, 친구야!", allow_space=True, allow_punctuation=True) is True

def test_has_batchim():
    assert has_batchim("강") is True
    assert has_batchim("가") is False
    assert has_batchim(" ") is False
    assert has_batchim("ㄱ") is False

def test_can_functions():
    assert can_cho("ㄱ") is True
    assert can_cho("ㅏ") is False
    assert can_jung("ㅏ") is True
    assert can_jong("ㄳ") is True
    assert can_jong("ㄸ") is False

def test_normalize():
    nfd_text = unicodedata.normalize('NFD', '한글')
    # 눈으로 보기엔 같지만 길이는 다름 (ㅎ, ㅏ, ㄴ, ㄱ, ㅡ, ㄹ = 6)
    assert len(nfd_text) == 6
    # NFC로 정규화
    nfc_text = normalize(nfd_text, form='NFC')
    assert len(nfc_text) == 2
    assert nfc_text == '한글'

    nfc_text = '한글'
    nfd_text = normalize(nfc_text, form='NFD')
    assert len(nfd_text) == 6

    with pytest.raises(Exception):
        normalize(123)
        normalize(None)