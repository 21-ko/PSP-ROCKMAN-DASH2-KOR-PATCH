import os
import sys
import re
import random
import ImageHill
from PIL import Image
import numpy as np
from scipy.spatial import KDTree

def compress(uncomp_data, down=False):
    # 출처: https://github.com/HilltopWorks/Mega-Man-Legends-2-Demo/blob/main/filesys.py
    # ...
            # test을 지우고 down을 작성,ref_size_coded이 선언되기 직전에 이 코드를 넣는다.
            # (의도적으로 압축률을 떨어뜨리는 코드)
            if down:
                down = max(0, min(down, 100))
                if random.random() < (down / 100):
                    continue
    # ...
    return control_buffer + body_buffer, len(control_buffer)
    
def extract_file_info(file_path):
    basename = os.path.basename(file_path)
    
    name, _ = os.path.splitext(basename)

    match = re.match(r"([^/\\]+)-0x([0-9a-fA-F]+)-(\d+)(\.uncomp)?", name)
    
    if not match:
        raise ValueError("잘못된 파일명 형식")

    dat_name = match.group(1)  # SELECT
    offset = f"0x{match.group(2)}"  # 0x0001c800
    file_kind = int(match.group(3))  # 3
    is_uncompressed = match.group(4) is not None  # .uncomp 여부

    return {
        "basename": name,
        "dat_name": dat_name,
        "offset": int(offset, 16),
        "file_kind": file_kind,
        "is_uncompressed": is_uncompressed
    }
    
def getColorCount(pxl_mode):
    return {4: 16, 8: 256}.get(pxl_mode, 0)

def closest(pixel, clut, color_dict, threshold=128):
    if pixel in color_dict:
        return color_dict[pixel]

    # 투명한 픽셀 처리
    if pixel[3] == 0:
        ALPHA_INDEX = next((i for i, c in enumerate(clut) if c[3] == 0), 0)
        color_dict[pixel] = ALPHA_INDEX
        return ALPHA_INDEX

    # clut에 동일한 색상이 있는 경우 해당 색상의 index 반환
    if pixel in clut:
        index = clut.index(pixel)
        color_dict[pixel] = index
        return index

    # 반투명 픽셀 처리
    if 0 < pixel[3] < 255:
        if pixel[3] < threshold:
            ALPHA_INDEX = next((i for i, c in enumerate(clut) if c[3] == 0), 0)
            color_dict[pixel] = ALPHA_INDEX
            return ALPHA_INDEX
        else:
            # threshold 이상의 알파값을 가진 경우 RGB 값 기준으로 최근접 색상 찾기
            r, g, b, _ = pixel
            tree = KDTree([c[:3] for c in clut])
            _, index = tree.query((r, g, b))
            color_dict[pixel] = index
            return index

    # 일반 픽셀 (불투명) 처리
    tree = KDTree([c[:3] for c in clut])
    _, index = tree.query(pixel[:3])

    color_dict[pixel] = index
    return index

def convertBITMAP(png_path, pxl_mode, clut_definition, clut_len=0, plus_offset=0, down=False):
    basename = os.path.splitext(os.path.basename(png_path))[0]
    file_info = extract_file_info(png_path)
    offset = file_info["offset"]
    clut_path = "./ORG/" + basename + ".bin"
    output_path = "../DAT/" + file_info["dat_name"] + ".BIN"
    is_comp = file_info["is_uncompressed"]

    image = Image.open(png_path)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
        
    png_width, png_height = image.size

    if clut_definition["CLUT_MODE"] != -1:
        with open(clut_definition["CLUT_FILE"], "rb") as clut_file:
            n_clut_entries = getColorCount(pxl_mode)
            clut = ImageHill.readCLUT(clut_file, clut_definition["CLUT_OFFSET"], n_clut_entries, clut_definition["CLUT_MODE"])

    color_dict = {}
    bitmap_data = bytearray()

    if pxl_mode == 4:
        for y in range(png_height):
            for x in range(png_width // 2):
                x1, y1 = x * 2, y
                x2, y2 = x * 2 + 1, y
                
                val1 = closest(image.getpixel((x1, y1)), clut, color_dict)
                val2 = closest(image.getpixel((x2, y2)), clut, color_dict)

                new_byte = val1 | (val2 << 4)
                bitmap_data.append(new_byte)

    elif pxl_mode == 8:
        for y in range(png_height):
            for x in range(png_width):
                val = closest(image.getpixel((x, y)), clut, color_dict)
                bitmap_data.append(val)

    if not is_comp:
        with open(output_path, "rb+") as file:
            file.seek(offset+0x30+plus_offset)
            file.write(bitmap_data)
    else:
        with open(clut_path, "rb") as file:
            clut_data = file.read(clut_len)
            
        comped_data, bits_len = compress(clut_data + bitmap_data, down)
    
        with open(output_path, "rb+") as file:
            file.seek(offset+8)
            pdsize = int.from_bytes(file.read(2), "little")
            pdsize *= 0x800
            pdsize -= 0x30
            
            file.seek(offset+0x24)
            file.write(bits_len.to_bytes(2, "little"))
            
            file.seek(offset+0x30+plus_offset)
            file.write(comped_data)
            if len(comped_data) <= pdsize:
                need_padding = pdsize - len(comped_data)
                if need_padding >= 0x800:
                    print("Warning!", png_path)
                file.write(need_padding * b'\x00')
            else:
                print("\aFUCK!", png_path, hex(pdsize), hex(len(comped_data)))
                sys.exit(1)
            
def convertTEMPBITMAP(image, pxl_mode, clut_definition):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
        
    png_width, png_height = image.size

    if clut_definition["CLUT_MODE"] != -1:
        with open(clut_definition["CLUT_FILE"], "rb") as clut_file:
            n_clut_entries = getColorCount(pxl_mode)
            clut = ImageHill.readCLUT(clut_file, clut_definition["CLUT_OFFSET"], n_clut_entries, clut_definition["CLUT_MODE"])

    color_dict = {}
    bitmap_data = bytearray()

    if pxl_mode == 4:
        for y in range(png_height):
            for x in range(png_width // 2):
                x1, y1 = x * 2, y
                x2, y2 = x * 2 + 1, y
                
                val1 = closest(image.getpixel((x1, y1)), clut, color_dict)
                val2 = closest(image.getpixel((x2, y2)), clut, color_dict)

                new_byte = val1 | (val2 << 4)
                bitmap_data.append(new_byte)

    elif pxl_mode == 8:
        for y in range(png_height):
            for x in range(png_width):
                val = closest(image.getpixel((x, y)), clut, color_dict)
                bitmap_data.append(val)

    return bitmap_data
    
def CropImg(image_path, x, y, w, h):
    img = Image.open(image_path)
    cropped_img = img.crop((x, y, x + w, y + h))
    return cropped_img
    
def combineIMAGES(clut_data, img1_bytes, img2_bytes, img3_bytes, img4_bytes, output_path, offset):
    # 256x256 크기의 빈 이미지 생성
    combined_img = bytearray(32768)

    # 각 이미지의 위치 정보 (이미지 데이터, x 좌표, y 좌표, 이미지 너비)
    img_info = [
        (img1_bytes, 0, 0, 208),      # img1 (너비 208)
        (img2_bytes, 0, 40, 208),     # img2 (너비 208)
        (img3_bytes, 0, 120, 208),    # img3 (너비 208)
        (img4_bytes, 208, 0, 48)      # img4 (너비 48)
    ]

    # 각 이미지를 결합된 이미지에 배치
    for img_bytes, x_pos, y_pos, img_width in img_info:
        img_height = len(img_bytes) * 2 // img_width  # 4비트라서 2픽셀당 1바이트 사용

        for y in range(img_height):
            for x in range(img_width):
                src_idx = (y * img_width + x) // 2
                if src_idx >= len(img_bytes):
                    continue
                
                dst_x = x_pos + x
                dst_y = y_pos + y
                dst_byte_index = (dst_y * 128) + (dst_x // 2)

                if dst_byte_index >= len(combined_img):
                    continue

                pixel_value = (img_bytes[src_idx] >> (4 * (1 - x % 2))) & 0x0F

                if dst_x % 2 == 0:
                    combined_img[dst_byte_index] = (pixel_value << 4) | (combined_img[dst_byte_index] & 0x0F)
                else:
                    combined_img[dst_byte_index] = (combined_img[dst_byte_index] & 0xF0) | pixel_value
    
    comped_data, bits_len = compress(clut_data + combined_img, 70)
    with open(output_path, 'rb+') as f:
        f.seek(offset+8)
        pdsize = int.from_bytes(f.read(2), "little")
        pdsize *= 0x800
        pdsize -= 0x30
        
        f.seek(offset+0x24)
        f.write(bits_len.to_bytes(2, "little"))
        
        f.seek(offset+0x30)  # + 헤더 크기
        f.write(comped_data)
        if len(comped_data) <= pdsize:
            need_padding = pdsize - len(comped_data)
            if need_padding >= 0x800:
                print("Warning!", output_path)
            f.write(need_padding * b'\x00')
        else:
            print("\aFUCK!")
            sys.exit(1)

    
# SUBSCN
subscC =          {
                            "CLUT_FILE":r"ORG/GAME-0x00030800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# GAME
GAME_C =      {
                            "CLUT_FILE":r"ORG/GAME-0x00030800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

# ST23T
ST23T1_C =          {
                            "CLUT_FILE":r"ORG/ST23T-0x00041000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }
                        
ST23T2_C =    {
                            "CLUT_FILE":r"ORG/ST23T-0x00043800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST23T3_C =    {
                            "CLUT_FILE":r"ORG/ST23T-0x00046800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# ST25T
ST25T_C =          {
                            "CLUT_FILE":r"ORG/ST25T-0x00049000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }
                        
ST25T2_C =          {
                            "CLUT_FILE":r"ORG/ST25T-0x0004d800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }
                        
# TITLE
TITLE_C =          {
                            "CLUT_FILE":r"ORG/TITLE-0x00005800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
TITLE5_0_C =          {
                            "CLUT_FILE":r"ORG/TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
TITLE5_1_C =          {
                            "CLUT_FILE":r"ORG/TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":1*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
TITLE5_2_C =          {
                            "CLUT_FILE":r"ORG/TITLE-0x0000f800-3.uncomp.bin",
                            "CLUT_OFFSET":2*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# SELECT
SELECT_C =          {
                            "CLUT_FILE":r"ORG/SELECT-0x00003800-2.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
SELECT3_C =  {
                            "CLUT_FILE":r"ORG/SELECT-0x0001c800-3.uncomp.bin",
                            "CLUT_OFFSET":0x0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
convertBITMAP("BMP/SUBSCN06-0x00000000-2.png", 4, subscC, 0, 0x800-0x30)
convertBITMAP("BMP/SUBSCN03-0x00001800-2.png", 4, subscC, 0, 0x800-0x30)
convertBITMAP("BMP/SUBSCN04-0x00000000-2.png", 4, subscC, 0, 0x800-0x30)

convertBITMAP("BMP/GAME-0x00030800-3.uncomp.png", 4, GAME_C, 0x100, down=20)

convertBITMAP("BMP/ST23T-0x00041000-3.uncomp.png", 4, ST23T1_C, 0x80)
convertBITMAP("BMP/ST23T-0x00043800-3.uncomp.png", 4, ST23T2_C, 0x80)
convertBITMAP("BMP/ST23T-0x00046800-3.uncomp.png", 4, ST23T3_C, 0x80)

convertBITMAP("BMP/ST25T-0x00049000-3.uncomp.png", 4, ST25T_C, 0x80)
convertBITMAP("BMP/ST25T-0x0004d800-3.uncomp.png", 4, ST25T2_C, 0x80)

convertBITMAP("BMP/TITLE/TITLE-0x00005800-3.uncomp.png", 8, TITLE_C, 0x200)
convertBITMAP("BMP/TITLE/TITLE-0x00008000-3.uncomp.png", 8, TITLE_C, down=30)
#convertBITMAP("BMP/TITLE/TITLE-0x0000b000-3.uncomp.png", 8, TITLE_C)
convertBITMAP("BMP/TITLE/TITLE-0x0000d800-3.uncomp.png", 8, TITLE_C, down=80)

# 특별한 경우
#convertBITMAP("BMP/TITLE-0x0000f800-3.uncomp.png", 4, TITLE5_C, 0xC0)
img1 = CropImg("BMP/TITLE-0x0000f800-3.uncomp.png", 0, 0, 208, 40)
img2 = CropImg("BMP/TITLE-0x0000f800-3.uncomp.png", 0, 40, 208, 80)
img3 = CropImg("BMP/TITLE-0x0000f800-3.uncomp.png", 0, 120, 208, 136)
img4 = CropImg("BMP/TITLE-0x0000f800-3.uncomp.png", 208, 0, 48, 256)
img1_bytes = convertTEMPBITMAP(img1, 4, TITLE5_0_C)
img2_bytes = convertTEMPBITMAP(img2, 4, TITLE5_1_C)
img3_bytes = convertTEMPBITMAP(img3, 4, TITLE5_2_C)
img4_bytes = convertTEMPBITMAP(img4, 4, TITLE5_1_C)
with open('ORG/TITLE-0x0000f800-3.uncomp.bin', "rb") as file:
    clut_data = file.read(0xC0)
combineIMAGES(clut_data, img1_bytes, img2_bytes, img3_bytes, img4_bytes, "../DAT/TITLE.BIN", 0x0000f800)

convertBITMAP("BMP/SELECT-0x00000000-3.uncomp.png", 4, SELECT_C, 0x20, down=80)
convertBITMAP("BMP/SELECT-0x00004800-3.uncomp.png", 4, SELECT_C, 0x20, down=84)

convertBITMAP("BMP/SELECT-0x0001c800-3.uncomp.png", 8, SELECT3_C, 0x200, down=70)
