import pytest
from hangeul.number import num2han

def test_num2han():
    # 기본 변환
    assert num2han(1234) == "천이백삼십사"
    assert num2han(1010) == "천십"
    
    # 만 단위 축약 (일만 -> 만)
    assert num2han(10000) == "만"
    assert num2han(15000) == "만오천"
    
    # 억 단위 (일억 유지)
    assert num2han(100000000) == "일억"
    
    # 큰 숫자 및 0 처리
    assert num2han(0) == "영"
    assert num2han(200010) == "이십만십"
    
    # 에러 처리
    with pytest.raises(ValueError):
        num2han("123a")