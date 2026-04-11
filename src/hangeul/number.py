from typing import Final

_NUM_MAP: Final = {
    "0": "", "1": "일", "2": "이", "3": "삼", "4": "사",
    "5": "오", "6": "육", "7": "칠", "8": "팔", "9": "구"
}
_UNIT_MAP: Final = ["", "십", "백", "천"]
_BLOCK_MAP: Final = ["", "만", "억", "조", "경", "해"]

def num2han(number: int | str) -> str:
    """
    숫자를 한글 읽기 방식으로 변환합니다.
    예: 1234 -> "천이백삼십사", 10001 -> "만일"
    """
    num_str = str(number).strip().replace(",", "")
    if not num_str.isdigit():
        if not num_str: return ""
        raise ValueError(f"숫자만 입력 가능합니다: {num_str}")
    
    if int(num_str) == 0:
        return "영"

    # 4자리씩 chunk로 쪼갬
    length = len(num_str)
    full_str = num_str.zfill(((length - 1) // 4 + 1) * 4)
    chunks = [full_str[i:i+4] for i in range(0, len(full_str), 4)]
    
    result = []
    num_chunks = len(chunks)
    
    for i, chunk in enumerate(chunks):
        chunk_res = ""
        for j, digit in enumerate(chunk):
            if digit == "0":
                continue
            
            unit = _UNIT_MAP[3 - j]
            val = _NUM_MAP[digit]
            
            # '일십', '일백', '일천' -> '십', '백', '천'으로 축약 (단, 일의 자리는 유지)
            if val == "일" and unit != "":
                chunk_res += unit
            else:
                chunk_res += val + unit
        
        if chunk_res:
            block_unit = _BLOCK_MAP[num_chunks - 1 - i]
            # '일만' 대신 '만'이 자연스러운 경우 처리
            if chunk_res == "일" and block_unit == "만":
                result.append(block_unit)
            else:
                result.append(chunk_res + block_unit)
                
    return "".join(result)