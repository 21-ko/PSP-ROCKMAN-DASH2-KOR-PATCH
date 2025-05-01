import re
import os
import sys
import struct

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
    
Moji_list = load_moji_list('MojiKor.tbl')

def txt_to_bin(input_file):
    global Moji_list
    command_table = {
        'FUNC': b'',
        'LINE': b'\xFC',
        'END': b'\xFF'
    }

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    block_data_list = []
    current_block = bytearray()

    for line in lines:
        line = line.strip('\n')

        if line.startswith("[BLOCK:"):
            if current_block:
                block_data_list.append(current_block)
            current_block = bytearray()
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
    if current_block:
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python txt2msg.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    basename = os.path.basename(input_file)
    basename_without_ext = os.path.splitext(basename)[0]
    
    parts = basename_without_ext.split('-')
    
    if len(parts) < 2 or not parts[1].startswith('0x'):
        print(f"Error: Invalid input filename format: {basename_without_ext}")
        print("Expected format: FILENAME-0xOFFSET")
        sys.exit(1)
    
    file_prefix = parts[0]
    offset_str = parts[1]
    
    try:
        offset = int(offset_str, 16)
    except ValueError:
        print(f"Error: Invalid offset format: {offset_str}")
        print("Expected format: 0xOFFSET (hexadecimal)")
        sys.exit(1)
        
    bin_file = os.path.join('DAT', f'{file_prefix}.BIN')
    if not os.path.exists(bin_file):
        print(f"Error: {bin_file} not found")
        sys.exit(1)
    
    binary_data = txt_to_bin(input_file)
    size = len(binary_data)
    with open(bin_file, 'r+b') as f:
        f.seek(offset + 8)
        org_pdsize = struct.unpack('<H', f.read(2))[0]
        max_size = org_pdsize * 0x800
        max_size -= 0x30  # 헤더 크기 빼기
        
        # 크기 검사
        if size > max_size:
            print(f"Error: Data size ({size} bytes) exceeds maximum allowed size ({max_size} bytes)")
            sys.exit(1)
        
        # 데이터 패딩
        padding_size = max_size - size
        padded_data = binary_data + b'\x00' * padding_size
        
        # 새 크기 업데이트
        f.seek(offset + 4)
        f.write(struct.pack('<H', size))
        
        # 패딩된 바이너리 데이터 쓰기 (offset + 0x30 위치에)
        f.seek(offset + 0x30)
        f.write(padded_data)
        
    print(f"Successfully updated {bin_file}")
    print(f"Original size: {size} bytes")
    print(f"Padded size: {max_size} bytes (added {padding_size} bytes of padding)")
    print(f"Original pdsize: 0x{org_pdsize:X} ({org_pdsize})")

if __name__ == "__main__":
    main()