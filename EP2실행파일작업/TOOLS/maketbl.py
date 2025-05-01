def create_table_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        chars = f.read().rstrip('”★')

    with open(output_file, 'w', encoding='utf-8') as f:
        value = 0
        for char in chars:
            if value == 0xEA:
                value += 0xF016
            if value == 0xF6D0:
                value += 0x30
            
            high = (value >> 8) & 0xFF
            low = value & 0xFF
            if value < 0xEA:
                f.write(f"{low:02X}={char}\n")
            else:
                f.write(f"{high:02X}{low:02X}={char}\n")
            value += 1
        f.write(f"4E=∼\n")
        f.write(f"4E=~\n")

if __name__ == "__main__":
    create_table_file("DATA/chars.txt", "Moji.tbl")