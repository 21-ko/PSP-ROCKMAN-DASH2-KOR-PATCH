import os
import re
import shutil
from pathlib import Path

def get_char_width(char):
    # 문자별 너비 정의
    width_table = {
        '0': 7+2, '1': 3+2, '2': 7+2, '3': 7+2, '4': 8+2, '5': 7+2,
        '6': 7+2, '7': 7+2, '8': 7+2, '9': 7+2, ',': 2+2, '.': 2+2,
        "'": 2+2, '"': 5+2, '!': 1+2, '?': 7+2, '(': 4+2, ')': 4+2, ':': 2+2,
        'A': 9+2, 'B': 8+2, 'C': 8+2, 'D': 8+2, 'E': 8+2, 'F': 8+2,
        'G': 8+2, 'H': 8+2, 'I': 1+2, 'J': 6+2, 'K': 7+2, 'L': 8+2,
        'M': 9+2, 'N': 7+2, 'O': 8+2, 'P': 8+2, 'Q': 9+2, 'R': 8+2,
        'S': 8+2, 'T': 9+2, 'U': 8+2, 'V': 9+2, 'W': 9+2, 'X': 8+2,
        'Y': 7+2, 'Z': 8+2, 'a': 6+2, 'b': 6+2, 'c': 6+2, 'd': 6+2,
        'e': 6+2, 'f': 5+2, 'g': 6+2, 'h': 6+2, 'i': 1+2, 'j': 4+2,
        'k': 6+2, 'l': 1+2, 'm': 7+2, 'n': 6+2, 'o': 7+2, 'p': 6+2,
        'q': 7+2, 'r': 4+2, 's': 6+2, 't': 5+2, 'u': 6+2, 'v': 5+2,
        'w': 9+2, 'x': 6+2, 'y': 5+2, 'z': 6+2, ' ': 6
    }
    
    return width_table.get(char, 12)

def calculate_text_width(text):
    return sum(get_char_width(char) for char in text)

def calculate_pos_x(text):
    clean_text = re.sub(r'<[^>]+>', '', text.rstrip('\n'))
    total_width = calculate_text_width(clean_text)
    x_pos = (320 - total_width) // 2
    return f"{max(0, x_pos):04X}"

def calculate_char_count(text):
    clean_text = re.sub(r'<[^>]+>', '', text.rstrip('\n'))
    total_width = calculate_text_width(clean_text)
    total_width = ((total_width // 12) + 1) * 12 if total_width % 12 != 0 else total_width
    return f"{(total_width // 12) + 1:02X}"

def process_block(block):
    lines = block.split('\n')
    text_line = None
    pos_line_idx = None

    for i, line in enumerate(lines):
        if '<POS' in line:
            pos_line_idx = i
        elif not line.startswith('<') and line.strip('\n'):
            text_line = line.rstrip('\n')

    if text_line and pos_line_idx is not None:
        current_pos = lines[pos_line_idx]
        pos_values = current_pos[5:-1]
        new_x_pos = calculate_pos_x(text_line)
        new_char_count = calculate_char_count(text_line)
        new_pos = f"<POS {new_x_pos}{pos_values[4:8]}{new_char_count}{pos_values[10:]}>"
        lines[pos_line_idx] = new_pos

    return '\n'.join(lines)

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('[BLOCK:')
    processed_blocks = []

    if blocks[0].strip('\n') == '':
        blocks = blocks[1:]

    for block in blocks:
        if block.strip('\n'):
            processed_blocks.append(process_block(f'[BLOCK:{block}'))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(processed_blocks))

def main():
    txt_dir = Path('TXT')
    eboot_dir = Path('EBOOT')
    eboot_dir.mkdir(exist_ok=True)

    list_path = Path('DATA/list.txt')
    if list_path.exists():
        with open(list_path, 'r', encoding='utf-8') as f:
            target_files = {line.strip() for line in f.readlines()}
    else:
        target_files = set()

    for txt_file in txt_dir.glob('*.txt'):
        output_file = eboot_dir / txt_file.name

        if txt_file.name in target_files:
            process_file(txt_file, output_file)
        else:
            shutil.copy(txt_file, output_file)

if __name__ == '__main__':
    main()
