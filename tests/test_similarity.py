from hangeul import jamo_similarity

def test_jamo_similarity():
    assert jamo_similarity("파이썬", "파이썬") == 1.0
    
    assert jamo_similarity("안녕", "안녀") > 0.8
    
    assert jamo_similarity("사과", "자동차") < 0.5
    
    assert jamo_similarity("사람", "사5람") > 0.8