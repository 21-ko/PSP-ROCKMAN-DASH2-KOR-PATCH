import re
import os
import sys

def load_moji_list(file_path):
    moji_list = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            value, key = line.strip('\n').split('=')
            value = value.strip('\n')
            try:
                moji_list[key] = bytes.fromhex(value)
            except ValueError:
                print(f"Invalid value: '{value}' in line: '{line.strip()}'")
    return moji_list
    
script_dir = os.path.dirname(os.path.abspath(__file__))
moji_file_path = os.path.join(script_dir, 'MojiKor.tbl')
Moji_list = load_moji_list(moji_file_path)

def txt_to_bin(input_file):
    global Moji_list
    command_table = {
        'FUNC': b'',
        'POS': b'\xfb\x06',
        'WAIT': b'\xfb\x08',
        'VWAIT': b'\xfb\x09',
        'COLOR': b'\xfb\x0a',
        'INIT_COLOR': b'\xfb\x0b',
        'SEL': b'\xfb\x0f',
        'PAGEKEY': b'\xfb\x18',
        'VOICELOAD': b'\xfb\x1a',
        'ITEM_NAME': b'\xfb\x20',
        'BUTTON': b'\xfb\x22',
        'ENDKEY': b'\xfb\x24',
        'SPACE': b'\xfb\x2e',
        'LINE': b'\xfc',
        'NEXTPAGE': b'\xfd\x00',
        'END': b'\xff'
    }

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    block_data_list = []
    current_block = None

    for line in lines:
        line = line.strip('\n')

        if line.startswith("[BLOCK:"):
            if current_block is not None:
                block_data_list.append(current_block)
            current_block = bytearray()
            continue

        if current_block is None:
            continue

        i = 0
        while i < len(line):
            if line[i:i+1] == '<':
                end_idx = line.find('>', i)
                if end_idx != -1:
                    cmd_content = line[i+1:end_idx]
                    parts = cmd_content.split()
                    cmd = parts[0]
                    
                    if cmd in command_table:
                        current_block.extend(command_table[cmd])
                        if len(parts) > 1:
                            param = ' '.join(parts[1:])
                            current_block.extend(bytes.fromhex(param))
                    else:
                        try:
                            current_block.extend(bytes.fromhex(cmd_content))
                        except ValueError:
                            print(f"Warning: Skipping invalid HEX value '{cmd_content}'")
                    
                    i = end_idx + 1
                else:
                    if line[i] in Moji_list:
                        current_block.extend(Moji_list[line[i]])
                    else:
                        print(f"Warning: Skipping unmapped character '{line[i]}'")
                    i += 1
            else:
                if line[i] in Moji_list:
                    current_block.extend(Moji_list[line[i]])
                else:
                    print(f"Warning: Skipping unmapped character '{line[i]}'")
                i += 1

    # 마지막 블록도 추가
    if current_block is not None:
        block_data_list.append(current_block)

    # 오프셋 테이블 생성
    num_blocks = len(block_data_list)
    offset_table_size = (num_blocks + 1) * 2  # +1 for EOF
    block_offsets = []
    current_offset = offset_table_size

    binary_data = bytearray()
    for block in block_data_list:
        block_offsets.append(current_offset)
        binary_data.extend(block)
        current_offset += len(block)
    block_offsets.append(current_offset)  # EOF 오프셋 추가

    # 오프셋 테이블 생성
    offset_table = bytearray()
    for offset in block_offsets:
        offset_table.extend(offset.to_bytes(2, 'little'))

    return offset_table + binary_data

def calculate_padded_size(size, block_size):
    return (size + block_size - 1) & ~(block_size - 1)
    
def write_header_to_header_bin(header, directory, offset):
    header_bin_path = os.path.join(directory, "HEADER.BIN")
    with open(header_bin_path, 'r+b') as f:
        f.seek(offset)
        f.write(header)

def main():
    if len(sys.argv) < 2:
        print("Usage: python txt2msg.py <input_file> <output_file>]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    binary_data = txt_to_bin(input_file)
    
    file_name_prefix = os.path.basename(input_file)[:4]
    
    if not file_name_prefix.isdigit():
        print("Error: The first 4 characters of the input file name must be digits.")
        sys.exit(1)
    
    sign_bytes = (0x12).to_bytes(4, 'little')
    
    size = len(binary_data)
    size_bytes = size.to_bytes(4, 'little')
    size += 0x30
    
    padded_size = calculate_padded_size(size, 0x800)
    padded_size_bytes = (padded_size // 0x800).to_bytes(4, 'little')
    remaining_size = padded_size - size
    
    bin_dummy_bytes = b'\x00' * 0x24
    padd_bytes = b'\x00' * remaining_size
    header = sign_bytes + size_bytes + padded_size_bytes + bin_dummy_bytes
    binary_data = binary_data + padd_bytes
    
    # 헤더를 HEADER.BIN에 쓰기
    offset = int(file_name_prefix) * 0x30
    output_file_directory = os.path.dirname(output_file)
    write_header_to_header_bin(header, output_file_directory, offset)

    with open(output_file, 'wb') as f:
        f.write(binary_data)

if __name__ == "__main__":
    main()