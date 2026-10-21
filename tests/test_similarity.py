from hangeul import similarity


def test_jamo_similarity():
    assert similarity("파이썬", "파이썬") == 1.0

    assert similarity("안녕", "안녀") > 0.8

    assert similarity("사과", "자동차") < 0.5

    assert similarity("사람", "사5람") > 0.8
