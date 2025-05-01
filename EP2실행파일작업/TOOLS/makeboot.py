import shutil

def read_file(file_path, start=None, size=None):
    with open(file_path, 'rb') as f:
        if start is not None and size is not None:
            f.seek(start)
            return f.read(size)
        return f.read()

def write_to_boot_bin(boot_bin_path, offset, data):
    with open(boot_bin_path, 'r+b') as f:
        f.seek(offset)
        f.write(data)

font_path = 'DATA/VRAM.PIX'
boot_bin_path = 'EBOOT.BIN'

font_data = read_file(font_path)

write_to_boot_bin(boot_bin_path, 0x00AAC2A0+0x2800, font_data)
