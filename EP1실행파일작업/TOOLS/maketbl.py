def create_table_file(input_file, pre_table_file, output_file):
    pre_table_content = []
    try:
        with open(pre_table_file, 'r', encoding='utf-8') as pre_file:
            pre_table_content = pre_file.readlines()
    except FileNotFoundError:
        print(f"경고: {pre_table_file} 파일을 찾을 수 없습니다. 새로운 내용만 생성합니다.")
    
    buffer = ["\n"]
    with open(input_file, 'r', encoding='utf-8') as f:
        chars = f.read().strip('★')
    
    value = 0xF828
    for char in chars:
        if value == 0xF8B3+1:
            value += 0x4D-1
        if value == 0xF9DC:
            value += 0x24
        
        high = (value >> 8) & 0xFF
        low = value & 0xFF
        buffer.append(f"{high:02X}{low:02X}={char}\n")
        value += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(pre_table_content)
        f.writelines(buffer)

if __name__ == "__main__":
    create_table_file(
        "./DATA/chars_onlykor.txt", 
        "./DATA/Moji_pre.tbl", 
        "./Moji.tbl"
    )