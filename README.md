# hangeul

파이썬용 한글 텍스트 처리 도구 모음입니다.

[![PyPI](https://img.shields.io/pypi/v/hangeul)](https://pypi.org/project/hangeul/)
[![Python](https://img.shields.io/pypi/pyversions/hangeul)](https://pypi.org/project/hangeul/)
[![Tests](https://github.com/NaNIsaac/hangeul/actions/workflows/tests.yml/badge.svg)](https://github.com/NaNIsaac/hangeul/actions/workflows/tests.yml)
[![License](https://img.shields.io/pypi/l/hangeul)](https://github.com/NaNIsaac/hangeul/blob/main/LICENSE)

**English summary.** `hangeul` is a dependency-free Python library (3.10+) for Korean text:
jamo split and assembly (`ㄱㅏㅂㅅㅇㅣ` -> `값이`), particle (josa) selection that handles numbers
and acronyms (`IBM이`, `7로`), initial-consonant (choseong) search, jamo-level similarity, and
Korean number reading (`1234` -> `천이백삼십사`).

## 설치

```bash
pip install hangeul
# 또는
uv add hangeul
```

## 빠른 시작

```python
import hangeul as han

# 조사 선택 (숫자, 영문 대문자 약어, 괄호 처리)
print(han.attach("IBM", "이/가"))           # IBM이
print(han.attach("SDK", "은/는"))           # SDK는
print(han.attach("7", "으로/로"))           # 7로
print(han.attach("애플(Apple)", "이/가"))   # 애플(Apple)이

# 자모 분해와 조합
print(han.disassemble("값이"))              # ㄱㅏㅂㅅㅇㅣ
print(han.assemble("ㄱㅏㅂㅅㅇㅣ"))        # 값이

# 초성 검색
print(han.matches("서강대학교", "ㅅㄱㄷ"))  # True
print(han.search_filter(["사과", "수박", "포도"], "ㅅㅂ"))  # ['수박']

# 자소 단위 유사도 (0.0 ~ 1.0)
print(han.similarity("값", "갑"))           # 0.75

# 숫자 읽기
print(han.num2han(1234567))                 # 백이십삼만사천오백육십칠
```

## API

### 조사

| 함수 | 설명 |
| --- | --- |
| `get_josa(word, pattern)` | `word` 뒤에 올 조사를 `pattern`(예: `"이/가"`, `"으로/로"`)에서 골라 반환합니다. 패턴의 앞뒤 순서는 상관없습니다. |
| `attach(word, pattern)` | `word`와 고른 조사를 이어 붙여 반환합니다. |

지원 패턴: 이/가, 은/는, 을/를, 와/과, 아/야, 나/이나, 란/이란, 랑/이랑, 라/이라, 예요/이에요,
로/으로, 로서/으로서, 로써/으로써, 로부터/으로부터. `로` 계열은 ㄹ 받침 뒤에서 `로`를 고릅니다.
그 밖의 두 항목 패턴은 `받침 있을 때/받침 없을 때` 순서로 해석합니다.
마지막 글자가 숫자이면 한국어 읽기(일, 이, 삼...)로, 영문 대문자 약어이면 알파벳 이름(에이, 비, 씨...)으로
판단합니다. 소문자 영단어는 받침 없음으로 취급하며, 끝의 괄호 부분은 무시합니다.

### 조합과 분해

| 함수 | 설명 |
| --- | --- |
| `disassemble(text)` | 완성형 한글을 자모로 분해합니다. 겹받침(`ㄳ`)과 이중모음(`ㅘ`)도 나눕니다. 한글이 아닌 문자는 그대로 둡니다. |
| `assemble(text)` | 자모열을 완성형 한글로 조합합니다. 겹받침, 이중모음, 연음을 처리합니다. |
| `qwerty2han(text)` | 두벌식 자판으로 입력한 영문 키 입력을 자모로 바꿉니다 (`"gksrmf"` -> `"ㅎㅏㄴㄱㅡㄹ"`). `assemble`과 함께 쓰면 한/영 전환을 잊고 친 글을 복원할 수 있습니다. |

### 검색과 유사도

| 함수 | 설명 |
| --- | --- |
| `get_chosung(text)` | 각 음절의 초성을 추출합니다 (`"한글"` -> `"ㅎㄱ"`). |
| `matches(target, query, choseong_only=False)` | 검색어가 초성만으로 이루어져 있으면 초성 비교, 아니면 자모 단위 부분 문자열 비교를 합니다. `choseong_only=True`면 검색어도 초성으로 바꿔 비교합니다. |
| `search_filter(targets, query)` | `matches`를 만족하는 항목만 남긴 리스트를 반환합니다. |
| `similarity(str1, str2)` | 두 문자열을 자모로 분해한 뒤 편집 거리로 0.0 ~ 1.0 사이의 유사도를 계산합니다. |

### 문자 판별

| 함수 | 설명 |
| --- | --- |
| `is_han(text, allow_space=True, allow_punctuation=False)` | 문자열이 한글(완성형과 호환 자모)로만 이루어졌는지 확인합니다. 공백과 문장 부호 허용 여부를 정할 수 있습니다. |
| `is_pure_han(text)` | 공백 없이 한글로만 이루어졌는지 확인합니다. |
| `has_batchim(char)` | 한 음절에 받침이 있는지 확인합니다. |
| `can_cho(char)`, `can_jung(char)`, `can_jong(char)` | 자모가 초성, 중성, 종성 자리에 올 수 있는지 확인합니다. |

### 숫자

| 함수 | 설명 |
| --- | --- |
| `num2han(number)` | 0 이상의 정수(또는 쉼표가 들어간 숫자 문자열)를 한국어 읽기로 바꿉니다. `10000`은 `"만"`, `100000000`은 `"일억"`이 됩니다. |

### 상수

`CHOSOENG`, `JUNGSOENG`, `JONGSOENG`: 유니코드 음절 순서대로 정렬된 초성(19), 중성(21), 종성(28, 첫 항목은 빈 문자열) 튜플.

## 개발

```bash
uv run pytest
uv run ruff check .
```

## 라이선스

MIT
