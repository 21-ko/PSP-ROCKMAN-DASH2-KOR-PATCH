import ImageHill
from PIL import Image
import numpy as np
from scipy.spatial import KDTree

def getColorCount(pxl_mode):
    return {4: 16, 8: 256}.get(pxl_mode, 0)

def closest(pixel, clut, color_dict, threshold=128):
    if pixel in color_dict:
        return color_dict[pixel]

    if pixel[3] == 0:
        ALPHA_INDEX = next((i for i, c in enumerate(clut) if c[3] == 0), 0)
        color_dict[pixel] = ALPHA_INDEX
        return ALPHA_INDEX

    if pixel in clut:
        index = clut.index(pixel)
        color_dict[pixel] = index
        return index

    if 0 < pixel[3] < 255:
        if pixel[3] < threshold:
            ALPHA_INDEX = next((i for i, c in enumerate(clut) if c[3] == 0), 0)
            color_dict[pixel] = ALPHA_INDEX
            return ALPHA_INDEX
        else:
            r, g, b, _ = pixel
            tree = KDTree([c[:3] for c in clut])
            _, index = tree.query((r, g, b))
            color_dict[pixel] = index
            return index

    tree = KDTree([c[:3] for c in clut])
    _, index = tree.query(pixel[:3])

    color_dict[pixel] = index
    return index

def convertBITMAP(png_path, offset, pxl_mode, clut_definition, output_path):
    image = Image.open(png_path)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
        
    png_width, png_height = image.size

    if clut_definition["CLUT_MODE"] != -1:
        with open(clut_definition["CLUT_FILE"], "rb") as clut_file:
            n_clut_entries = getColorCount(pxl_mode)
            clut = ImageHill.readCLUT(clut_file, clut_definition["CLUT_OFFSET"], n_clut_entries, clut_definition["CLUT_MODE"])

    color_dict = {}  # 색상 매핑 캐시
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

    with open(output_path, "rb+") as bitmap_file:
        bitmap_file.seek(offset)
        bitmap_file.write(bitmap_data)
        
def combineIMAGES(img1_bytes, img2_bytes, output_path, offset):
    combined_img = bytearray(32768)
    
    for i in range(len(img1_bytes)):
        combined_img[i] = img1_bytes[i]
    
    img2_width = 32
    img2_height = 160
    x_offset = 224
    y_offset = 0
    
    for y in range(img2_height):
        for x in range(0, img2_width, 2):
            src_pos = (y * img2_width + x) // 2
            
            if x + 1 < img2_width:
                src_byte = img2_bytes[src_pos]
                
                dst_row = y + y_offset
                dst_col = x + x_offset
                dst_pos = (dst_row * 256 + dst_col) // 2
                
                combined_img[dst_pos] = src_byte
            else:
                src_byte = img2_bytes[src_pos]
                low_nibble = src_byte & 0x0F
                
                dst_row = y + y_offset
                dst_col = x + x_offset
                dst_pos = (dst_row * 256 + dst_col) // 2
                
                combined_img[dst_pos] = (combined_img[dst_pos] & 0xF0) | low_nibble
    
    with open(output_path, 'rb+') as f:
        f.seek(offset)
        f.write(combined_img)

        
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

# COMMON
# SUBSCN
STATUS_C =          {
                            "CLUT_FILE":r"../OUTCOMMON/GAME/0013_GAME.CLT",
                            "CLUT_OFFSET":2*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# TITLE
TITLE_C =          {
                            "CLUT_FILE":r"ORG/0001_TITLE.PIX",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
TITLE5_C =          {
                            "CLUT_FILE":r"ORG/0005_TITLE.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
TITLE6_C =          {
                            "CLUT_FILE":r"ORG/TITLE06_SPECIAL.CLT",  # 마지막 색상을 위한 특별한 컬러 테이블
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
TITLE7_C =          {
                            "CLUT_FILE":r"ORG/0007_TITLE.PIX",
                            "CLUT_OFFSET":3*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# DAT
# ST04T
# ...
# ST18T          
ST18T_C =          {
                            "CLUT_FILE":r"ORG/0065_ST18T.PIX",
                            "CLUT_OFFSET":2*0x20,  # 최대 4
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
convertBITMAP("BMP/0000_SUBSCN_ADD.PNG", 0, 4, STATUS_C, "ORG/0000_SUBSCN_ADD.PIX")
convertBITMAP("BMP/0001_SUBSCN_ADD.PNG", 0, 4, STATUS_C, "ORG/0001_SUBSCN_ADD.PIX")
convertBITMAP("BMP/0003_SUBSCN.PNG", 0, 4, STATUS_C, "ORG/0003_SUBSCN.PIX")
convertBITMAP("BMP/0008_SUBSCN.PNG", 0, 4, STATUS_C, "ORG/0008_SUBSCN.PIX")
#convertBITMAP("BMP/0001_TITLE.PNG", 0x200, 8, TITLE_C, "ORG/0001_TITLE.PIX")
#convertBITMAP("BMP/0002_TITLE.PNG", 0, 8, TITLE_C, "ORG/0002_TITLE.PIX")
convertBITMAP("BMP/0003_TITLE.PNG", 0, 8, TITLE_C, "ORG/0003_TITLE.PIX")
convertBITMAP("BMP/0004_TITLE.PNG", 0, 8, TITLE_C, "ORG/0004_TITLE.PIX")
convertBITMAP("BMP/0005_TITLE.PNG", 0x60, 4, TITLE5_C, "ORG/0005_TITLE.PIX")
convertBITMAP("BMP/0006_TITLE.PNG", 0x40, 4, TITLE6_C, "ORG/0006_TITLE.PIX")
convertBITMAP("BMP/0007_TITLE.PNG", 0xC0, 4, TITLE7_C, "ORG/0007_TITLE.PIX")

convertBITMAP("BMP/0011_GAME.PNG", 0, 4, STATUS_C, "ORG/0011_GAME.PIX")
#convertBITMAP("BMP/0012_GAME.PNG", 0, 4, GAME_12_C, "ORG/0012_GAME.PIX")
convertBITMAP("BMP/0038_ST04T.PNG", 0, 4, STATUS_C, "ORG/0038_ST04T.PIX")

convertBITMAP("BMP/0065_ST18T.PNG", 0x100, 4, ST18T_C, "ORG/0065_ST18T.PIX")
convertBITMAP("BMP/0065_ST18T.PNG", 0x100, 4, ST18T_C, "ORG/0024_ST55T.PIX")
convertBITMAP("BMP/0065_ST18T.PNG", 0x100, 4, ST18T_C, "ORG/0065_ST1804T.PIX")
convertBITMAP("BMP/0065_ST18T.PNG", 0x100, 4, ST18T_C, "ORG/0067_ST1802T.PIX")
                        
ST2CT_BASE_C =          {
                            "CLUT_FILE":r"ORG/0008_ST2CT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST2CT_C =          {
                            "CLUT_FILE":r"ORG/0013_ST2CT.CLT",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST1BT_C =          {
                            "CLUT_FILE":r"ORG/0010_ST1BT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST5AT_C =          {
                            "CLUT_FILE":r"ORG/0013_ST5AT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST5BT_C =          {
                            "CLUT_FILE":r"ORG/0014_ST5BT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST59T_C =          {
                            "CLUT_FILE":r"ORG/0017_ST59T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST00T_C =          {
                            "CLUT_FILE":r"ORG/0018_ST00T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST3FT_C =          {
                            "CLUT_FILE":r"ORG/0018_ST3FT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST1FT_C =          {
                            "CLUT_FILE":r"ORG/0035_ST1FT.PIX",
                            "CLUT_OFFSET":1*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST3BT_C =          {
                            "CLUT_FILE":r"ORG/0043_ST3BT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST0AT_C =          {
                            "CLUT_FILE":r"ORG/0054_ST0AT.CLT",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST1AT_C =          {
                            "CLUT_FILE":r"ORG/0018_ST1AT.PIX",
                            "CLUT_OFFSET":1*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST0CT18_C =          {
                            "CLUT_FILE":r"ORG/0027_ST0CT.CLT",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST0CT48_C =          {
                            "CLUT_FILE":r"ORG/0048_ST0CT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

#convertBITMAP("BMP/0008_ST2CT.PNG", 0x100, 4, ST2CT_BASE_C, "ORG/0008_ST2CT.PIX")
# 특수
img1 = CropImg("BMP/0008_ST2CT.PNG", 0, 0, 256, 256)
img2 = CropImg("BMP/0008_ST2CT.PNG", 224, 0, 32, 160)
img1_bytes = convertTEMPBITMAP(img1, 4, ST2CT_BASE_C)
img2_bytes = convertTEMPBITMAP(img2, 4, ST2CT_C)
combineIMAGES(img1_bytes, img2_bytes, "ORG/0008_ST2CT.PIX", 0x100)

convertBITMAP("BMP/0010_ST1BT.PNG", 0x40, 4, ST1BT_C, "ORG/0010_ST1BT.PIX")  # 1
convertBITMAP("BMP/0010_ST1BT.PNG", 0x40, 4, ST1BT_C, "ORG/0011_ST1B01T.PIX")  # 1
convertBITMAP("BMP/0013_ST5AT.PNG", 0x20, 4, ST5AT_C, "ORG/0013_ST5AT.PIX")
convertBITMAP("BMP/0014_ST5BT.PNG", 0x20, 4, ST5BT_C, "ORG/0014_ST5BT.PIX")
convertBITMAP("BMP/0017_ST59T.PNG", 0x20, 4, ST59T_C, "ORG/0017_ST59T.PIX")
convertBITMAP("BMP/0018_ST00T.PNG", 0x60, 4, ST00T_C, "ORG/0018_ST00T.PIX")
convertBITMAP("BMP/0018_ST3FT.PNG", 0x20, 4, ST3FT_C, "ORG/0018_ST3FT.PIX")
convertBITMAP("BMP/0035_ST1FT.PNG", 0x80, 4, ST1FT_C, "ORG/0035_ST1FT.PIX")  # 2
convertBITMAP("BMP/0035_ST1FT.PNG", 0x80, 4, ST1FT_C, "ORG/0042_ST3001T.PIX")  # 2
convertBITMAP("BMP/0035_ST1FT.PNG", 0x80, 4, ST1FT_C, "ORG/0042_ST30T.PIX")  # 2
convertBITMAP("BMP/0043_ST3BT.PNG", 0x100, 4, ST3BT_C, "ORG/0043_ST3BT.PIX")
convertBITMAP("BMP/0047_ST0AT.PNG", 0x20, 4, ST0AT_C, "ORG/0047_ST0AT.PIX")
convertBITMAP("BMP/0018_ST0CT.PNG", 0x20, 4, ST0CT18_C, "ORG/0018_ST0CT.PIX")  # 3
convertBITMAP("BMP/0018_ST0CT.PNG", 0x20, 4, ST0CT18_C, "ORG/0018_ST47T.PIX")  # 3
convertBITMAP("BMP/0048_ST0CT.PNG", 0x20, 4, ST0CT48_C, "ORG/0048_ST0CT.PIX")  # 4
convertBITMAP("BMP/0048_ST0CT.PNG", 0x20, 4, ST0CT48_C, "ORG/0048_ST47T.PIX")  # 4
convertBITMAP("BMP/0018_ST1AT.PNG", 0x40, 4, ST1AT_C, "ORG/0018_ST1AT.PIX")  # 5
convertBITMAP("BMP/0018_ST1AT.PNG", 0x40, 4, ST1AT_C, "ORG/0018_ST1A01T.PIX")  # 5

                        
ST57T4_C =          {
                            "CLUT_FILE":r"ORG/0004_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T5_C =          {
                            "CLUT_FILE":r"ORG/0005_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T6_C =          {
                            "CLUT_FILE":r"ORG/0006_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T7_C =          {
                            "CLUT_FILE":r"ORG/0007_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T8_C =          {
                            "CLUT_FILE":r"ORG/0008_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T9_C =          {
                            "CLUT_FILE":r"ORG/0009_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T10_C =          {
                            "CLUT_FILE":r"ORG/0010_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T11_C =          {
                            "CLUT_FILE":r"ORG/0011_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T12_C =          {
                            "CLUT_FILE":r"ORG/0012_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T13_C =          {
                            "CLUT_FILE":r"ORG/0013_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T14_C =          {
                            "CLUT_FILE":r"ORG/0014_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T15_C =          {
                            "CLUT_FILE":r"ORG/0015_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T16_C =          {
                            "CLUT_FILE":r"ORG/0016_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T17_C =          {
                            "CLUT_FILE":r"ORG/0017_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T18_C =          {
                            "CLUT_FILE":r"ORG/0018_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T19_C =          {
                            "CLUT_FILE":r"ORG/0019_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T20_C =          {
                            "CLUT_FILE":r"ORG/0020_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
convertBITMAP("BMP/staff/0004_ST57T.PNG", 0x20, 4, ST57T4_C, "ORG/0004_ST57T.PIX")
convertBITMAP("BMP/staff/0005_ST57T.PNG", 0x20, 4, ST57T5_C, "ORG/0005_ST57T.PIX")
convertBITMAP("BMP/staff/0006_ST57T.PNG", 0x20, 4, ST57T6_C, "ORG/0006_ST57T.PIX")
convertBITMAP("BMP/staff/0007_ST57T.PNG", 0x20, 4, ST57T7_C, "ORG/0007_ST57T.PIX")
convertBITMAP("BMP/staff/0008_ST57T.PNG", 0x20, 4, ST57T8_C, "ORG/0008_ST57T.PIX")
convertBITMAP("BMP/staff/0009_ST57T.PNG", 0x20, 4, ST57T9_C, "ORG/0009_ST57T.PIX")
convertBITMAP("BMP/staff/0010_ST57T.PNG", 0x20, 4, ST57T10_C, "ORG/0010_ST57T.PIX")
convertBITMAP("BMP/staff/0011_ST57T.PNG", 0x20, 4, ST57T11_C, "ORG/0011_ST57T.PIX")
convertBITMAP("BMP/staff/0012_ST57T.PNG", 0x20, 4, ST57T12_C, "ORG/0012_ST57T.PIX")
convertBITMAP("BMP/staff/0013_ST57T.PNG", 0x20, 4, ST57T13_C, "ORG/0013_ST57T.PIX")
convertBITMAP("BMP/staff/0014_ST57T.PNG", 0x20, 4, ST57T14_C, "ORG/0014_ST57T.PIX")
convertBITMAP("BMP/staff/0015_ST57T.PNG", 0x20, 4, ST57T15_C, "ORG/0015_ST57T.PIX")
convertBITMAP("BMP/staff/0016_ST57T.PNG", 0x20, 4, ST57T16_C, "ORG/0016_ST57T.PIX")
convertBITMAP("BMP/staff/0017_ST57T.PNG", 0x20, 4, ST57T17_C, "ORG/0017_ST57T.PIX")
convertBITMAP("BMP/staff/0018_ST57T.PNG", 0x20, 4, ST57T18_C, "ORG/0018_ST57T.PIX")
convertBITMAP("BMP/staff/0019_ST57T.PNG", 0x20, 4, ST57T19_C, "ORG/0019_ST57T.PIX")
convertBITMAP("BMP/staff/0020_ST57T.PNG", 0x20, 4, ST57T20_C, "ORG/0020_ST57T.PIX")