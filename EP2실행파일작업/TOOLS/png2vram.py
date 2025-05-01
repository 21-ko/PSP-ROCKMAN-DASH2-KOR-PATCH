from PIL import Image
import numpy as np
import struct

rgba_pal = [
    (0, 0, 0, 0),
    (225, 216, 208, 255),
    (146, 144, 152, 255),
    (75, 80, 96, 255)
]

def rgba_to_index(rgba):
    for i, color in enumerate(rgba_pal):
        if rgba == color:
            return i
    print(f"경고: {rgba} 색상이 팔레트에 존재하지 않습니다.")
    return 0

def bit_combine(tp1, tp2, size):
    out = np.zeros(size, dtype=np.uint32)
    
    for cnt in range(size):
        out[cnt] = (tp1[cnt] & 0x33333333) | ((tp2[cnt] & 0x33333333) << 2)
    
    return out

def png_to_values(png_file):
    img = Image.open(png_file)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    all_pixels = [rgba_to_index(img.getpixel((x, y))) for y in range(img.height) for x in range(img.width)]

    values = []
    for i in range(0, len(all_pixels), 8):
        value = 0
        for j in range(8):
            if i + j < len(all_pixels):
                value |= (all_pixels[i + j] & 0xF) << (j * 4)
        values.append(value)
    
    return values, img.width, img.height

def pngs_to_combined_pix(png_file1, png_file2, output_file):
    values1, width1, height1 = png_to_values(png_file1)
    values2, width2, height2 = png_to_values(png_file2)
    
    if width1 != width2 or height1 != height2:
        print(f"경고: 이미지 크기가 다릅니다. font1: {width1}x{height1}, font2: {width2}x{height2}")
    
    size = max(len(values1), len(values2))
    if len(values1) < size:
        values1.extend([0] * (size - len(values1)))
    if len(values2) < size:
        values2.extend([0] * (size - len(values2)))
    
    np_values1 = np.array(values1, dtype=np.uint32)
    np_values2 = np.array(values2, dtype=np.uint32)
    
    combined_values = bit_combine(np_values1, np_values2, size)
    
    with open(output_file, 'wb') as f:
        for value in combined_values:
            f.write(struct.pack('<I', int(value)))

if __name__ == '__main__':
    input_png1 = 'DATA/font1.png'
    input_png2 = 'DATA/font2.png'
    output_pix = 'DATA/VRAM.PIX'
    pngs_to_combined_pix(input_png1, input_png2, output_pix)