import os
import re
import shutil
from pathlib import Path

def get_char_width(char):
    width_table = {
        ' ': 6
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
        if '<FB06' in line:
            pos_line_idx = i
        elif not line.startswith('<') and line.strip('\n'):
            text_line = line.rstrip('\n')

    if text_line and pos_line_idx is not None:
        current_pos = lines[pos_line_idx]
        
        tag_parts = current_pos.split(' ', 1)
        tag_name = tag_parts[0][1:]
        
        params = tag_parts[1][:-1] if len(tag_parts) > 1 else ""
        
        new_x_pos = calculate_pos_x(text_line)
        new_char_count = calculate_char_count(text_line)
        
        y_pos = params[4:8] if len(params) >= 8 else ""
        remaining = params[10:] if len(params) >= 10 else ""
        new_pos = f"<{tag_name} {new_x_pos}{y_pos}{new_char_count}{remaining}>"
            
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
    subs_dir = Path('TXT')
    eboot_dir = Path('EBOOT')
    eboot_dir.mkdir(exist_ok=True)

    list_path = Path('DATA/list.txt')
    if list_path.exists():
        with open(list_path, 'r', encoding='utf-8') as f:
            target_files = {line.strip('\n') for line in f.readlines()}
    else:
        target_files = set()

    for txt_file in subs_dir.glob('*.txt'):
        output_file = eboot_dir / txt_file.name

        if txt_file.name in target_files:
            process_file(txt_file, output_file)
        else:
            shutil.copy(txt_file, output_file)

if __name__ == '__main__':
    main()
