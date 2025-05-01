import re
import sys
import os

DEBUG = False

def read_short(file, position):
    file.seek(position)
    return int.from_bytes(file.read(2), 'little')

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
    
Moji_list = load_moji_list('Moji.tbl')

def txt_to_bin(input_file, base_offset, base_offset_2=None, plus=None):
    global Moji_list
    a = 2
    b = b''
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
                            try:
                                current_block.extend(bytes.fromhex(param))
                            except ValueError:
                                print(f"Error in file {input_file}: Invalid hex value '{param}' in line '{line}'")
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
                        print(f"Warning: '{line[i]}'")
                        current_block.extend(b'\x0E')
                    i += 1
            else:
                if line[i] in Moji_list:
                    current_block.extend(Moji_list[line[i]])
                else:
                    print(f"Warning: '{line[i]}'")
                    current_block.extend(b'\x0E')
                i += 1

    if current_block is not None:
        block_data_list.append(current_block)

    if base_offset_2 != None:
        a = 4
        b = b'\xFF\xFF\x00\x00'

    # 오프셋 테이블 생성
    num_blocks = len(block_data_list)
    offset_table_size = (num_blocks + 1) * a  # +1 for EOF
    block_offsets = []
    
    if base_offset_2 != None:
        current_offset = base_offset_2 - base_offset + plus
    else:
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
        offset_table.extend(offset.to_bytes(a, 'little'))

    return b+offset_table, binary_data
    
def extract_offset_from_filename(filename):
    match = re.search(r'0x[0-9A-Fa-f]+', filename)
    if match:
        return int(match.group(0), 16)
    raise ValueError("Invalid filename format. Filename must be in '0x??????.txt' format.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python txt2bin.py <input_folder>")
        return
    
    input_folder = sys.argv[1]
    eboot_file = "EBOOT.BIN"
    base_offset = 0x4E2770  # .data 위치
    base_offset_2 = 0xAEEAA0+0x40000
    next_data_offset = 0
    
    txt_files = []
    for file in sorted(os.listdir(input_folder)):
        if file.endswith(".txt"):
            txt_files.append(os.path.join(input_folder, file))
    
    if not txt_files:
        print(f"Error: No txt files found in {input_folder}")
        return
    
    print(f"Found {len(txt_files)} txt files to process")
    
    for input_file in txt_files:
        try:
            ptr_offset = extract_offset_from_filename(input_file)
        except ValueError as e:
            print(f"Error in file {input_file}: {e}")
            continue
        
        if DEBUG:
            print(f"Processing file: {input_file}")
        
        offset_table, binary_data = txt_to_bin(input_file, None)
        binary_data = offset_table + binary_data
        
        with open(eboot_file, "rb+") as f:
            # first_offset 읽기
            pos = base_offset + ptr_offset
            first_offset = read_short(f, pos)
            
            # size 값 읽기
            size_pos = pos + first_offset - 2
            size = read_short(f, size_pos)
            
            # 새 데이터가 size 제한을 넘지 않는지 확인
            if len(binary_data) <= size:
                # 새 데이터 쓰기
                f.seek(base_offset + ptr_offset)
                f.write(binary_data)
                
                # 데이터가 size보다 작으면 나머지를 0으로 채우기
                if len(binary_data) < size:
                    padding = bytes([0] * (size - len(binary_data)))
                    f.write(padding)
                
                if DEBUG:
                    print(f"Successfully wrote {len(binary_data)} bytes (size limit: {size})")
                    print(f"Offset: 0x{ptr_offset:X}")
            else:
                # 16바이트 정렬을 위해 next_data_offset 조정
                if next_data_offset % 16 != 0:
                    padding_needed = 16 - (next_data_offset % 16)
                    next_data_offset += padding_needed
                    if DEBUG:
                        print(f"Aligning to 16-byte boundary: added {padding_needed} bytes padding")
                
                # 데이터 크기가 제한을 초과하는 경우 대체 영역 사용
                if DEBUG:
                    print(f"Error: New data size ({len(binary_data)} bytes) exceeds limit ({size} bytes)")
                    print(f"Using alternate storage area at offset 0x{base_offset_2 + next_data_offset:X}")
                
                # 새로운 위치에 대한 오프셋 테이블 및 바이너리 데이터 생성
                offset_table, binary_data = txt_to_bin(input_file, pos, base_offset_2, next_data_offset)
                
                # 원래 위치에 오프셋 테이블 쓰기
                f.seek(base_offset + ptr_offset)
                f.write(offset_table)
                if len(offset_table) < size:
                    padding = bytes([0] * (size - len(offset_table)))
                    f.write(padding)
                
                # 새로운 위치에 바이너리 데이터 쓰기
                data_write_position = base_offset_2 + next_data_offset
                f.seek(data_write_position)
                if DEBUG:
                    print(f"Writing binary data at: 0x{data_write_position:X} (16-byte aligned)")
                f.write(binary_data)
                
                # 다음 데이터를 위한 오프셋 업데이트
                next_data_offset += len(binary_data)
                
                # 다음 데이터도 16바이트 정렬을 위한 준비
                # 여기서는 계산만 하고, 실제 정렬은 다음 파일 처리 시 수행
                if DEBUG:
                    print(f"Current next_data_offset: 0x{next_data_offset:X}")
                    if next_data_offset % 16 != 0:
                        align_padding = 16 - (next_data_offset % 16)
                        print(f"Next data will need {align_padding} bytes padding for 16-byte alignment")
        
        if DEBUG:
            print(f"Completed processing file: {input_file}")
            print("-" * 50)
    
    print(f"All {len(txt_files)} files processed successfully")

if __name__ == "__main__":
    main()