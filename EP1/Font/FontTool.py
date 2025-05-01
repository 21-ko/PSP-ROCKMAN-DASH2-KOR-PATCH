import numpy as np
from PIL import Image
import sys

WIDTH = 256
HEIGHT = 252

palette = {
    0: (0, 0, 0, 0),
    1: (248, 248, 248, 255),
    2: (160, 168, 176, 255),
    3: (72, 80, 96, 255),
}

def rgba_to_index(rgba):
    for k, v in palette.items():
        if tuple(rgba) == v:
            return k
    return 0

def bit_split(combined, size):
    low_plane = np.zeros(size, dtype=np.uint32)
    high_plane = np.zeros(size, dtype=np.uint32)

    for cnt in range(size):
        low_plane[cnt] = combined[cnt] & 0x33333333
        high_plane[cnt] = (combined[cnt] >> 2) & 0x33333333

    return low_plane, high_plane

def bit_combine(low_plane, high_plane, size):
    out = np.zeros(size, dtype=np.uint32)

    for cnt in range(size):
        out[cnt] = (low_plane[cnt] & 0x33333333) | ((high_plane[cnt] & 0x33333333) << 2)

    return out

def make_image(data, width, height, filename):
    img = Image.new('RGBA', (width, height))
    pixels = img.load()

    for i in range(width * height):
        val = (data[i >> 3] >> ((i & 7) * 4)) & 0xF
        color = palette.get(val & 0x3, (0, 0, 0, 0))
        pixels[i % width, i // width] = color

    img.save(filename)

def read_image(filename, width, height):
    img = Image.open(filename).convert('RGBA')
    pixels = img.load()
    data = np.zeros((width * height + 7) // 8, dtype=np.uint32)

    for i in range(width * height):
        color = pixels[i % width, i // width]
        index = rgba_to_index(color)
        shift = (i & 7) * 4
        data[i >> 3] |= (index & 0x3) << shift

    return data

def split():
    with open("FONT.BIN", "rb") as f:
        raw = np.frombuffer(f.read(), dtype=np.uint32)
    size = raw.size
    low_plane, high_plane = bit_split(raw, size)

    make_image(low_plane, WIDTH, HEIGHT, "FONT1.PNG")
    make_image(high_plane, WIDTH, HEIGHT, "FONT2.PNG")
    print("분할 완료: FONT1.PNG, FONT2.PNG 생성됨")

def combine():
    low_plane = read_image("FONT1.PNG", WIDTH, HEIGHT)
    high_plane = read_image("FONT2.PNG", WIDTH, HEIGHT)
    size = (WIDTH * HEIGHT) // 8

    combined = bit_combine(low_plane, high_plane, size)
    with open("FONT.BIN", "wb") as f:
        f.write(combined.tobytes())
    print("병합 완료: FONT.BIN 생성됨")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python FontTool.py [split|combine]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "split":
        split()
    elif cmd == "combine":
        combine()
    else:
        print("알 수 없는 명령입니다. split 또는 combine 중 하나를 사용하세요.")
