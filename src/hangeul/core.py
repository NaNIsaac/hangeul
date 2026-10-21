from .constants import 초성, 중성, 종성, 겹받침맵, 복합모음맵, 쿼티한글맵

# 성능을 위한 인덱스 맵 미리 생성 (O(1) lookup)
_CHO_IDX = {char: i for i, char in enumerate(초성)}
_JUNG_IDX = {char: i for i, char in enumerate(중성)}
_JONG_IDX = {char: i for i, char in enumerate(종성)}
_SPLIT_JONG_MAP = {v: k for k, v in 겹받침맵.items()}
_SPLIT_JUNG_MAP = {v: k for k, v in 복합모음맵.items()}


def qwerty2han(text: str) -> str:
    """영문 쿼티 문자열을 한글 자모 문자열로 변환합니다."""
    return "".join(쿼티한글맵.get(char, char) for char in text)


def assemble(text: str) -> str:
    """자소 단위로 분리된 문자열을 완성형 한글로 조합합니다."""
    cho_idx, jung_idx, jong_idx = -1, -1, 0
    result: list[str] = []

    def make_syllable(c, r, t):
        return chr(0xAC00 + (c * 21 * 28) + (r * 28) + t)

    def flush():
        nonlocal cho_idx, jung_idx, jong_idx
        if cho_idx != -1 and jung_idx != -1:
            result.append(make_syllable(cho_idx, jung_idx, jong_idx))
        elif cho_idx != -1:
            result.append(초성[cho_idx])
        elif jung_idx != -1:
            result.append(중성[jung_idx])
        cho_idx, jung_idx, jong_idx = -1, -1, 0

    for char in text:
        # 1. 자음 처리
        if char in _CHO_IDX or char in _JONG_IDX:
            if cho_idx != -1 and jung_idx != -1:
                if jong_idx == 0:  # 현재 받침 없음
                    if char in _JONG_IDX:
                        jong_idx = _JONG_IDX[char]
                    else:  # 종성 불가 자음 (ㄸ, ㅃ, ㅉ)
                        flush()
                        cho_idx = _CHO_IDX.get(char, -1)
                else:  # 현재 받침 있음 -> 겹받침 가능성 확인
                    cur_jong = 종성[jong_idx]
                    if (cur_jong, char) in 겹받침맵:
                        jong_idx = _JONG_IDX[겹받침맵[(cur_jong, char)]]
                    else:  # 겹받침 불가 -> 새 글자로
                        flush()
                        if char in _CHO_IDX:
                            cho_idx = _CHO_IDX[char]
                        else:
                            result.append(char)
            else:  # 초성만 있거나, 모음만 있거나, 새로 시작
                flush()
                if char in _CHO_IDX:
                    cho_idx = _CHO_IDX[char]
                else:
                    result.append(char)

        # 2. 모음 처리
        elif char in _JUNG_IDX:
            # 받침이 있는 상태에서 모음이 오면 연음 처리 (예: 값이 -> 갑시)
            if jong_idx != 0:
                cur_jong_char = 종성[jong_idx]
                if cur_jong_char in _SPLIT_JONG_MAP:  # 겹받침인 경우 분리
                    f_jong, s_cho = _SPLIT_JONG_MAP[cur_jong_char]
                    result.append(make_syllable(cho_idx, jung_idx, _JONG_IDX[f_jong]))
                    cho_idx, jung_idx, jong_idx = _CHO_IDX[s_cho], _JUNG_IDX[char], 0
                else:  # 일반 받침은 다음 초성으로 이동
                    result.append(make_syllable(cho_idx, jung_idx, 0))
                    cho_idx, jung_idx, jong_idx = (
                        _CHO_IDX.get(cur_jong_char, -1),
                        _JUNG_IDX[char],
                        0,
                    )

            elif cho_idx != -1:  # 초성만 있는 상태에서 모음
                if jung_idx == -1:
                    jung_idx = _JUNG_IDX[char]
                else:  # 복합 모음 가능성 (ㅗ + ㅏ = ㅘ)
                    cur_jung = 중성[jung_idx]
                    if (cur_jung, char) in 복합모음맵:
                        jung_idx = _JUNG_IDX[복합모음맵[(cur_jung, char)]]
                    else:
                        flush()
                        jung_idx = _JUNG_IDX[char]
            else:  # 초성 없는 모음 단독
                if jung_idx != -1:
                    cur_jung = 중성[jung_idx]
                    if (cur_jung, char) in 복합모음맵:
                        jung_idx = _JUNG_IDX[복합모음맵[(cur_jung, char)]]
                        flush()
                    else:
                        flush()
                        jung_idx = _JUNG_IDX[char]
                else:
                    jung_idx = _JUNG_IDX[char]

        # 3. 기타 문자 (숫자, 영문, 특수문자 등)
        else:
            flush()
            result.append(char)

    flush()
    return "".join(result)


def disassemble(text: str) -> str:
    """
    완성형 한글 문자열을 개별 자소 단위로 완전히 분리합니다.
    (예: '값' -> 'ㄱㅏㅂㅅ', '과' -> 'ㄱㅗㅏ')
    """
    result: list[str] = []

    for char in text:
        # 1. 완성형 한글인 경우 (가 ~ 힣)
        if "가" <= char <= "힣":
            num = ord(char) - 0xAC00
            c = num // 588
            r = (num % 588) // 28
            t = num % 28

            # 초성 추가
            result.append(초성[c])

            # 중성 분리 (ㅘ -> ㅗ, ㅏ)
            jung_char = 중성[r]
            if jung_char in _SPLIT_JUNG_MAP:
                result.extend(_SPLIT_JUNG_MAP[jung_char])
            else:
                result.append(jung_char)

            # 종성 분리 (ㄳ -> ㄱ, ㅅ)
            if t > 0:
                jong_char = 종성[t]
                if jong_char in _SPLIT_JONG_MAP:
                    result.extend(_SPLIT_JONG_MAP[jong_char])
                else:
                    result.append(jong_char)

        # 2. 이미 분리된 자제나 기타 문자인 경우
        else:
            if char in _SPLIT_JUNG_MAP:
                result.extend(_SPLIT_JUNG_MAP[char])
            elif char in _SPLIT_JONG_MAP:
                result.extend(_SPLIT_JONG_MAP[char])
            else:
                result.append(char)

    return "".join(result)


if __name__ == "__main__":
    # 1. 복합 문자 분리 테스트
    print(disassemble("값이"))  # 결과: "ㄱㅏㅂㅅㅇㅣ"

    # 2. 역변환 (Round-trip) 테스트
    raw = "값이"
    dis = disassemble(raw)
    ass = assemble(dis)
    print(f"{raw} -> {dis} -> {ass}")  # 결과: 값이 -> ㄱㅏㅂㅅㅇㅣ -> 값이

    # 3. 복합 모음 테스트
    print(disassemble("왜 뭐가"))
