"""Inputs the API must reject or leave alone."""

import pytest

import hangeul as han


@pytest.mark.parametrize("pattern", ["이", "", "이/가/을"])
def test_josa_pattern_needs_two_forms(pattern):
    with pytest.raises(ValueError, match="지원하지 않는 조사 패턴"):
        han.get_josa("값", pattern)


@pytest.mark.parametrize("value", [-1, "-5", "12a", 1.5, True, None])
def test_num2han_rejects_non_counts(value):
    with pytest.raises(ValueError, match="숫자만 입력 가능"):
        han.num2han(value)


def test_unpaired_jamo_survive_assemble():
    assert han.assemble("ㅏㅏ") == "ㅏㅏ"


def test_non_hangul_query_matches_nothing():
    assert han.matches("한글", "abc") is False
    assert han.search_filter(["사과", "수박"], "abc") == []
