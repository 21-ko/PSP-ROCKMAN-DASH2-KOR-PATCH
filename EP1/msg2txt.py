import os
import sys
import struct
from functools import partial

def read_byte(f):
    return struct.unpack('B', f.read(1))[0]

def read_short(f):
    return struct.unpack('>H', f.read(2))[0]

def control_code_legacy(f, control_code_full, length):
    codes = ''
    
    for _ in range(length):
        code = read_byte(f)
        codes += f'{code:02X}'

    alias = f'{control_code_full:04X}'
    return f'<{alias}>' if not codes else f'<{alias} {codes}>'

# 제어 코드 목록
LEGACY_CODES =   {
    0xFB00 :  0,
    0xFB01 :  3,
    0xFB02 :  1,
    0xFB03 :  0,
    0xFB04 :  2,
    0xFB05 :  2,
    0xFB06 :  6,
    0xFB07 :  1,
    0xFB08 :  2,
    0xFB09 :  1,
    0xFB0a :  1,
    0xFB0b :  0,
    0xFB0c :  0,
    0xFB0d :  4,
    0xFB0e :  1,
    0xFB0f :  1,
    0xFB10 :  5,
    0xFB11 :  3,
    0xFB12 :  2,
    0xFB13 :  2,
    0xFB14 :  3,
    0xFB15 :  9,
    0xFB16 :  11,
    0xFB17 :  0,
    0xFB18 :  0,
    0xFB19 :  2,
    0xFB1a :  3,
    0xFB1b :  0,
    0xFB1c :  0,
    0xFB1d :  0,
    0xFB1e :  2,
    0xFB1f :  0,
    0xFB20 :  1,
    0xFB21 :  0,
    0xFB22 :  1,
    0xFB23 :  0,
    0xFB24 :  0,
    0xFB25 :  0,
    0xFB26 :  2,
    0xFB27 :  2,
    0xFB28 :  4,
    0xFB29 :  0,
    0xFB2a :  2,
    0xFB2b :  0,
    0xFB2c :  1,
    0xFB2d :  1,
    0xFB2e :  1,
    0xFB2f :  1,
    0xFB30 :  1,
    0xFB31 :  0,
    0xFB32 :  1,
    0xFB33 :  1,
    0xFB34 :  2,
    0xFB35 :  2,
    0xFB36 :  2,
    0xFB37 :  4,
    0xFD00 : 3
    }

CONTROL_CODE_LIST = {code: partial(control_code_legacy, length=a) for code, a in LEGACY_CODES.items()}

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
                if 0x00 <= byte_val <= 0xF7:
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
                #elif byte_val == 0xFD:
                #    text_parts.append('<FD>')
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
                    print(f"\aHuh? - Value: {hex(byte_val)} | Offset: {hex(f.tell() - 1)}")

            decoded_text = ''.join([moji_dict.get(byte, f' UNKCHAR_{int(byte.hex(), 16):02X} ') if isinstance(byte, bytes) else byte for byte in text_parts])
            decoded_texts.append((i, decoded_text))

    return decoded_texts

def write_to_file(file_name, texts):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for i, text in texts:
                file.write(f'[BLOCK: {i:04X}]\n')
                file.write(f'{text}')
                file.write(f'{NEW_LINE}\n\n')
    except FileNotFoundError:
        print(f"{file_name} not found.")

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
        
    pointers = get_pointers(filename, offset)
    pointer_diff = calculate_difference(pointers)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moji_tbl_path = os.path.join(script_dir, 'Moji.tbl')
    if not os.path.exists(moji_tbl_path):
        print("Character list file is missing")
        sys.exit(1)
    moji_dict = load_moji_table(moji_tbl_path)
    
    decoded_texts = decode_with_moji_and_controlcode(filename, offset, moji_dict, is_func, pointers, pointer_diff)
    write_to_file(output_file, decoded_texts)

if __name__ == '__main__':
    main()