import os
import sys
import struct
from functools import partial

def read_byte(f):
    return struct.unpack('B', f.read(1))[0]

def read_short(f):
    return struct.unpack('>H', f.read(2))[0]

def read_long(f):
    return struct.unpack('>I', f.read(4))[0]

# 제어 코드 0xfb06
def get_pos(f, _):
    b2 = read_short(f)
    b3 = read_short(f)
    b4 = read_byte(f)
    b5 = read_byte(f)
    return f'<POS {b2:04X}{b3:04X}{b4:02X}{b5:02X}>'

# 제어 코드 0xfb15
def _1_52_(f, _):
    b2 = ord(f.read(1))
    codes = ''.join([f'{read_short(f):04X}' for _ in range(5)])
    return f'<FB15 {b2:02X}{codes}>'

# 기본적인 제어 코드를 처리하는 함수
# a는 데이터의 길이, b는 데이터 크기, c는 포맷 처리 여부
def control_code_legacy(f, control_code_full, a, b, c):
    codes = ''
    if a == 'len':  # 길이를 받아오는 경우
        length = read_byte(f)
        a = length
        codes = f'{length:02X}'

    for _ in range(a):
        code = read_byte(f) if b == 1 else (read_short(f) if b == 2 else read_long(f))
        codes += f'{code:02X}' if b == 1 else f'{code:04X}' if b == 2 else f'{code:08X}'

    alias = c if isinstance(c, str) else f'{control_code_full:04X}'
    return f'<{alias}>' if not codes else f'<{alias} {codes}>'

# 제어 코드 목록
LEGACY_CODES = {
    0xfb04: (1, 2, 0),
    0xfb05: (2, 1, 0),
    0xfb07: (2, 1, 0),
    0xfb08: (1, 2, 'WAIT'),
    0xfb09: (1, 1, 'VWAIT'),
    0xfb0a: (1, 1, 'COLOR'),
    0xfb0b: (0, 0, 'INIT_COLOR'),
    0xfb0c: (0, 0, 0),
    0xfb0d: (4, 1, 0),
    0xfb0e: (1, 1, 0),
    0xfb0f: (1, 1, 'SEL'),
    0xfb10: ('len', 2, 0),
    0xfb11: ('len', 1, 0),
    0xfb12: (2, 1, 0),
    0xfb13: (7, 1, 0),
    0xfb16: (4, 1, 0),
    0xfb18: (0, 0, 'PAGEKEY'),
    0xfb19: (1, 2, 0),
    0xfb1a: (1, 4, 'VOICELOAD'),
    0xfb1b: (0, 0, 0),
    0xfb1c: (0, 0, 0),
    0xfb1d: (0, 0, 0),
    0xfb1f: (0, 0, 0),
    0xfb20: (2, 1, 'ITEM_NAME'),
    0xfb21: (1, 1, 0),
    0xfb22: (1, 1, 'BUTTON'),
    0xfb23: (1, 1, 0),
    0xfb24: (0, 0, 'ENDKEY'),
    0xfb25: (1, 1, 0),
    0xfb26: (2, 1, 0),
    0xfb27: (2, 1, 0),
    0xfb28: (4, 1, 0),
    0xfb29: (1, 1, 0),
    0xfb2a: (5, 1, 0),
    0xfb2b: (0, 0, 0),
    0xfb2c: (1, 1, 0),
    0xfb2e: (1, 1, 'SPACE'),
    0xfb30: (1, 1, 0),
    0xfb31: (0, 0, 0),
    0xfb33: (1, 1, 0),
    0xfb34: (2, 1, 0),
    0xfb35: (2, 1, 0),
    0xfb37: (5, 1, 0),
    0xfb39: ('len', 2, 0),
    0xfb3c: (429, 1, 0),
    0xfb3d: (0, 0, 0),
    0xfb3e: (2, 1, 0),
    0xfb3f: (3, 1, 0),
    0xfb40: (2, 1, 0),
    0xfb41: (3, 1, 0),
    0xfb42: (7, 1, 0),
    0xfb44: (1, 1, 0),
    0xfb45: (1, 1, 0),
    0xfb47: (4, 1, 0),
    0xfb48: (1, 1, 0),
    0xfb49: (1, 1, 0),
    0xfb4a: (1, 1, 0),
    0xfb4b: (1, 1, 0),
    0xfb4c: ('len', 2, 0),
    0xfd00: (3, 1, 'NEXTPAGE')
}

CONTROL_CODE_LIST = {code: partial(control_code_legacy, a=a, b=b, c=c) for code, (a, b, c) in LEGACY_CODES.items()}
CONTROL_CODE_LIST[0xfb06] = get_pos
CONTROL_CODE_LIST[0xfb15] = _1_52_

# 문자 테이블을 로드하는 함수
def load_moji_table(file_path):
    moji_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip('\n').split('=')
                key_bytes = bytes.fromhex(key)
                moji_dict[key_bytes] = value
    return moji_dict

NEW_LINE = '\n'

def get_pointers(filename, offset):
    with open(filename, 'rb') as f:
        f.seek(offset)
        pointer_count = struct.unpack('H', f.read(2))[0] // 2
        f.seek(offset)
        return [struct.unpack('H', f.read(2))[0] for _ in range(pointer_count)]

def calculate_difference(pointers):
    return [pointers[i + 1] - pointers[i] for i in range(len(pointers) - 1)]

def decode_with_moji_and_controlcode(filename, offset, moji_dict, is_func, pointers, pointer_diff):
    with open(filename, 'rb') as f:
        decoded_texts = []
        
        for i, diff in enumerate(pointer_diff):
            f.seek(offset + pointers[i])
            text_parts = []

            # 각 대사마다 func가 있는 경우
            if is_func == 1 and diff > 0:
                start_code = read_short(f)
                text_parts.append(f'<FUNC {start_code:04X}>')

            last_was_control_code = False

            for _ in range(diff):
                byte = f.read(1)
                byte_val = ord(byte)

                # 일반 텍스트 처리
                if 0x00 <= byte_val <= 0xE9:
                    text_parts.append(byte)
                    last_was_control_code = False
                # 2바이트 문자라면 추가로 1바이트를 더 읽음
                elif 0xF8 <= byte_val <= 0xFA:
                    text_parts.append(byte + f.read(1))
                    last_was_control_code = False
                # 제어 코드 처리
                elif byte_val in [0xFB, 0xFD]:
                    b1 = f.read(1)
                    control_code = (byte_val << 8) + ord(b1)
                    control_code_func = CONTROL_CODE_LIST.get(control_code)

                    if not last_was_control_code:
                        text_parts.append(NEW_LINE)

                    if control_code_func:
                        text_parts.append(control_code_func(f, control_code))
                        text_parts.append(NEW_LINE)
                    else:
                        text_parts.append(f'Unrecognized control code: 0x{control_code:04x}')
                    last_was_control_code = True
                # 줄 바꿈 처리
                elif byte_val == 0xFC:
                    text_parts.append('<LINE>' + NEW_LINE)
                # 특수 문자 처리 (루비 등)
                elif byte_val == 0xFE:
                    byte = f.read(1)
                    byte_val = ord(byte)

                    if 0x00 <= byte_val <= 0xE9:
                        text_parts.append(byte)
                        last_was_control_code = False
                    elif 0xF8 <= byte_val <= 0xFA:
                        byte += f.read(1)
                        text_parts.append(byte)
                        last_was_control_code = False

                    x = read_byte(f)
                    y = read_byte(f)
                    for _ in range(x):
                        rubi_char = f.read(1)
                # 문장의 끝 처리
                elif byte_val == 0xFF:
                    if text_parts and text_parts[-1] == (NEW_LINE):
                        text_parts.pop()
                    text_parts.append(NEW_LINE + '<END>')
                    break
                else:
                    print(f"\aHuh?  {hex(byte_val)}")

            decoded_text = ''.join([moji_dict.get(byte, '?') if isinstance(byte, bytes) else byte for byte in text_parts])
            decoded_texts.append((i, decoded_text))

    return decoded_texts

def write_to_file(file_name, texts, pointers):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for (i, text), pointer in zip(texts, pointers):
                #file.write(f'[BLOCK: {i:04X} | {pointer:04X}]\n')
                file.write(f'[BLOCK: {i:04X}]\n')
                file.write(f'{text}')
                file.write(f'{NEW_LINE}\n\n')
    except FileNotFoundError:
        print(f"{file_name} not found.")

# 명령줄 인자로 받은 오프셋 값을 해석하는 함수
def parse_off_param(offset_param):
    if '+' in offset_param:
        return sum(int(value, 16) if '0x' in value else int(value) for value in offset_param.split('+'))
    return int(offset_param, 16) if offset_param.startswith('0x') else int(offset_param)

def main():
    if len(sys.argv) < 4:
        print("Usage: python msg2txt.py <input_file> <output_file> <offset_param> [<is_func>]")
        sys.exit(1)

    filename, output_file, offset_param = sys.argv[1:4]
    is_func = int(sys.argv[4]) if len(sys.argv) > 4 else False
    if is_func < 0 or is_func >= 2:
        print("Invalid option")
        sys.exit(1)

    offset = parse_off_param(offset_param)

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 포인터와 포인터 간의 차이를 계산하여 텍스트 구간 설정
    pointers = get_pointers(filename, offset)
    pointer_diff = calculate_difference(pointers)
    
    # 문자 테이블 파일 로드
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moji_tbl_path = os.path.join(script_dir, 'Moji.tbl')
    if not os.path.exists(moji_tbl_path):
        print("Character list file is missing")
        sys.exit(1)
    moji_dict = load_moji_table(moji_tbl_path)
    
    # 파일을 디코딩하여 텍스트 추출 및 출력 파일로 저장
    decoded_texts = decode_with_moji_and_controlcode(filename, offset, moji_dict, is_func, pointers, pointer_diff)
    write_to_file(output_file, decoded_texts, pointers)

if __name__ == '__main__':
    main()