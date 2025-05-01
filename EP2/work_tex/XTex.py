import ImageHill
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil

# COMMOM
# SUBSCN
STATUS_C =          {
                            "CLUT_FILE":r"OUT/0013_GAME.CLT",
                            "CLUT_OFFSET":2*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
SUBSCN_P = {
                            "PXL_FILE":r"ORG_BAK/0000_SUBSCN_ADD.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
SUBSCN1_P = {
                            "PXL_FILE":r"ORG_BAK/0001_SUBSCN_ADD.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
SUBSCN3_P = {
                            "PXL_FILE":r"ORG_BAK/0003_SUBSCN.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
SUBSCN8_P = {
                            "PXL_FILE":r"ORG_BAK/0008_SUBSCN.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

# TITLE
TITLE_C =          {
                            "CLUT_FILE":r"ORG_BAK/0001_TITLE.PIX",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

TITLE_P = {
                            "PXL_FILE":r"ORG_BAK/0001_TITLE.PIX",
                            "PXL_OFFSET":0x200,
                            "WIDTH":480,
                            "HEIGHT":68,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE2_P = {
                            "PXL_FILE":r"ORG_BAK/0002_TITLE.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":480,
                            "HEIGHT":68,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE3_P = {
                            "PXL_FILE":r"ORG_BAK/0003_TITLE.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":480,
                            "HEIGHT":68,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE4_P = {
                            "PXL_FILE":r"ORG_BAK/0004_TITLE.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":480,
                            "HEIGHT":20,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE5_C =          {
                            "CLUT_FILE":r"ORG_BAK/0005_TITLE.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

TITLE5_P = {
                            "PXL_FILE":r"ORG_BAK/0005_TITLE.PIX",
                            "PXL_OFFSET":0x60,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
TITLE6_C =          {
                            "CLUT_FILE":r"ORG_BAK/TITLE06_SPECIAL.CLT",  # 마지막 색상을 위한 특별한 컬러 테이블
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

TITLE6_P = {
                            "PXL_FILE":r"ORG_BAK/0006_TITLE.PIX",
                            "PXL_OFFSET":0x40,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
TITLE7_C =          {
                            "CLUT_FILE":r"ORG_BAK/0007_TITLE.PIX",
                            "CLUT_OFFSET":3*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

TITLE7_P = {
                            "PXL_FILE":r"ORG_BAK/0007_TITLE.PIX",
                            "PXL_OFFSET":0xC0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
GAME11_P = {
                            "PXL_FILE":r"ORG_BAK/0011_GAME.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

# DAT
# ST04T
ST04T_P = {
                            "PXL_FILE":r"ORG_BAK/0038_ST04T.PIX",
                            "PXL_OFFSET":0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

# ST18T
ST18T_P = {
                            "PXL_FILE":r"ORG_BAK/0065_ST18T.PIX",
                            "PXL_OFFSET":0x100,
                            "WIDTH":256,
                            "HEIGHT":112,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST18T_C =          {
                            "CLUT_FILE":r"ORG_BAK/0065_ST18T.PIX",
                            "CLUT_OFFSET":2*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ImageHill.convertImage(SUBSCN_P, STATUS_C, "BMP/0000_SUBSCN_ADD.PNG", False)
ImageHill.convertImage(SUBSCN1_P, STATUS_C, "BMP/0001_SUBSCN_ADD.PNG", False)
ImageHill.convertImage(SUBSCN3_P, STATUS_C, "BMP/0003_SUBSCN.PNG", False)
ImageHill.convertImage(SUBSCN8_P, STATUS_C, "BMP/0008_SUBSCN.PNG", False)
ImageHill.convertImage(TITLE_P, TITLE_C, "BMP/0001_TITLE.PNG", False)
ImageHill.convertImage(TITLE2_P, TITLE_C, "BMP/0002_TITLE.PNG", False)
ImageHill.convertImage(TITLE3_P, TITLE_C, "BMP/0003_TITLE.PNG", False)
ImageHill.convertImage(TITLE4_P, TITLE_C, "BMP/0004_TITLE.PNG", False)
ImageHill.convertImage(TITLE5_P, TITLE5_C, "BMP/0005_TITLE.PNG", False)
ImageHill.convertImage(TITLE6_P, TITLE6_C, "BMP/0006_TITLE.PNG", False)
ImageHill.convertImage(TITLE7_P, TITLE7_C, "BMP/0007_TITLE.PNG", False)
ImageHill.convertImage(GAME11_P, STATUS_C, "BMP/0011_GAME.PNG", False)
#ImageHill.convertImage(GAME12_P, GAME12_C, "BMP/0012_GAME.PNG", False)
ImageHill.convertImage(ST04T_P, STATUS_C, "BMP/0038_ST04T.PNG", False)
ImageHill.convertImage(ST18T_P, ST18T_C, "BMP/0065_ST18T.PNG", False)

# ST2CT
ST2CT_P = {
                            "PXL_FILE":r"ORG_BAK/0008_ST2CT.PIX",
                            "PXL_OFFSET":0x100,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST2CT_BASE_C =          {
                            "CLUT_FILE":r"ORG_BAK/0008_ST2CT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST2CT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0013_ST2CT.CLT",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST1BT
ST1BT_P = {
                            "PXL_FILE":r"ORG_BAK/0010_ST1BT.PIX",
                            "PXL_OFFSET":0x40,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST1BT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0010_ST1BT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# ST1B01T
ST1B01T_P = {
                            "PXL_FILE":r"ORG_BAK/0011_ST1B01T.PIX",
                            "PXL_OFFSET":0x40,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
# ST5AT
ST5AT_P = {
                            "PXL_FILE":r"ORG_BAK/0013_ST5AT.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":128,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST5AT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0013_ST5AT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST5BT
ST5BT_P = {
                            "PXL_FILE":r"ORG_BAK/0014_ST5BT.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":128,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST5BT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0014_ST5BT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST59T
ST59T_P = {
                            "PXL_FILE":r"ORG_BAK/0017_ST59T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":128,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST59T_C =          {
                            "CLUT_FILE":r"ORG_BAK/0017_ST59T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST00T
ST00T_P = {
                            "PXL_FILE":r"ORG_BAK/0018_ST00T.PIX",
                            "PXL_OFFSET":0x60,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST00T_C =          {
                            "CLUT_FILE":r"ORG_BAK/0018_ST00T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST3FT
ST3FT_P = {
                            "PXL_FILE":r"ORG_BAK/0018_ST3FT.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST3FT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0018_ST3FT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST1FT
ST1FT_P = {
                            "PXL_FILE":r"ORG_BAK/0035_ST1FT.PIX",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":112,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST1FT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0035_ST1FT.PIX",
                            "CLUT_OFFSET":1*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# ST3001T
ST3001T_P = {
                            "PXL_FILE":r"ORG_BAK/0042_ST3001T.PIX",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":112,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
# ST3001T
ST30T_P = {
                            "PXL_FILE":r"ORG_BAK/0042_ST30T.PIX",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":112,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
# ST3BT
ST3BT_P = {
                            "PXL_FILE":r"ORG_BAK/0043_ST3BT.PIX",
                            "PXL_OFFSET":0x100,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST3BT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0043_ST3BT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
# ST0AT
ST0AT_P = {
                            "PXL_FILE":r"ORG_BAK/0047_ST0AT.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST0AT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0054_ST0AT.CLT",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# ST0CT
ST0CT18_P = {
                            "PXL_FILE":r"ORG_BAK/0018_ST0CT.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST0CT18_C =          {
                            "CLUT_FILE":r"ORG_BAK/0027_ST0CT.CLT",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ST0CT48_P = {
                            "PXL_FILE":r"ORG_BAK/0048_ST0CT.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST0CT48_C =          {
                            "CLUT_FILE":r"ORG_BAK/0048_ST0CT.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# ST1AT
ST1AT_P = {
                            "PXL_FILE":r"ORG_BAK/0018_ST1AT.PIX",
                            "PXL_OFFSET":0x40,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST1AT_C =          {
                            "CLUT_FILE":r"ORG_BAK/0018_ST1AT.PIX",
                            "CLUT_OFFSET":1*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

# ST47T
ST47T18_P = {
                            "PXL_FILE":r"ORG_BAK/0018_ST47T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

ST47T48_P = {
                            "PXL_FILE":r"ORG_BAK/0048_ST47T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
# 특수
os.makedirs("./BMP/TEMP", exist_ok=True)
ImageHill.convertImage(ST2CT_P, ST2CT_BASE_C, "BMP/TEMP/0008_BASE_ST2CT.PNG", False)
ImageHill.convertImage(ST2CT_P, ST2CT_C, "BMP/TEMP/0008_ST2CT.PNG", False)
image_1 = Image.open('BMP/TEMP/0008_ST2CT.PNG')
image_2 = Image.open('BMP/TEMP/0008_BASE_ST2CT.PNG')
crop_area = (224, 0, 224 + 32, 0 + 160)
cropped_image = image_1.crop(crop_area)
image_2.paste(cropped_image, (224, 0))
image_2.save('BMP/0008_ST2CT.PNG')
shutil.rmtree("./BMP/TEMP")

ImageHill.convertImage(ST1BT_P, ST1BT_C, "BMP/0010_ST1BT.PNG", False)  # 1
#ImageHill.convertImage(ST1B01T_P, ST1BT_C, "BMP/0011_ST1B01T.PNG", False)  # ST1BT 중복 이미지
ImageHill.convertImage(ST5AT_P, ST5AT_C, "BMP/0013_ST5AT.PNG", False)
ImageHill.convertImage(ST5BT_P, ST5BT_C, "BMP/0014_ST5BT.PNG", False)
ImageHill.convertImage(ST59T_P, ST59T_C, "BMP/0017_ST59T.PNG", False)
ImageHill.convertImage(ST00T_P, ST00T_C, "BMP/0018_ST00T.PNG", False)
ImageHill.convertImage(ST3FT_P, ST3FT_C, "BMP/0018_ST3FT.PNG", False)
ImageHill.convertImage(ST1FT_P, ST1FT_C, "BMP/0035_ST1FT.PNG", False)  # 2
#ImageHill.convertImage(ST3001T_P, ST1FT_C, "BMP/0042_ST3001T.PNG", False)  # ST1FT 중복 이미지
#ImageHill.convertImage(ST30T_P, ST1FT_C, "BMP/0042_ST30T.PNG", False)  # ST1FT 중복 이미지
ImageHill.convertImage(ST3BT_P, ST3BT_C, "BMP/0043_ST3BT.PNG", False)
ImageHill.convertImage(ST0AT_P, ST0AT_C, "BMP/0047_ST0AT.PNG", False)
ImageHill.convertImage(ST0CT18_P, ST0CT18_C, "BMP/0018_ST0CT.PNG", False)  # 3
#ImageHill.convertImage(ST47T18_P, ST0CT18_C, "BMP/0018_ST47T.PNG", False)  # ST0CT18 중복 이미지
ImageHill.convertImage(ST0CT48_P, ST0CT48_C, "BMP/0048_ST0CT.PNG", False)  # 4
#ImageHill.convertImage(ST47T48_P, ST0CT48_C, "BMP/0048_ST47T.PNG", False)  # ST0CT48 중복 이미지
ImageHill.convertImage(ST1AT_P, ST1AT_C, "BMP/0018_ST1AT.PNG", False)  # 5
#ImageHill.convertImage(ST1A01T_P, ST1A01T_C, "BMP/0018_ST1A01T.PNG", False)  # ST01AT 중복 이미지

# ST57T
ST57T4_P = {
                            "PXL_FILE":r"ORG_BAK/0004_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T4_C =          {
                            "CLUT_FILE":r"ORG_BAK/0004_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T5_P = {
                            "PXL_FILE":r"ORG_BAK/0005_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T5_C =          {
                            "CLUT_FILE":r"ORG_BAK/0005_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T6_P = {
                            "PXL_FILE":r"ORG_BAK/0006_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T6_C =          {
                            "CLUT_FILE":r"ORG_BAK/0006_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T7_P = {
                            "PXL_FILE":r"ORG_BAK/0007_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T7_C =          {
                            "CLUT_FILE":r"ORG_BAK/0007_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T8_P = {
                            "PXL_FILE":r"ORG_BAK/0008_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T8_C =          {
                            "CLUT_FILE":r"ORG_BAK/0008_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T9_P = {
                            "PXL_FILE":r"ORG_BAK/0009_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T9_C =          {
                            "CLUT_FILE":r"ORG_BAK/0009_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ST57T10_P = {
                            "PXL_FILE":r"ORG_BAK/0010_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T10_C =          {
                            "CLUT_FILE":r"ORG_BAK/0010_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T11_P = {
                            "PXL_FILE":r"ORG_BAK/0011_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T11_C =          {
                            "CLUT_FILE":r"ORG_BAK/0011_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T12_P = {
                            "PXL_FILE":r"ORG_BAK/0012_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T12_C =          {
                            "CLUT_FILE":r"ORG_BAK/0012_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T13_P = {
                            "PXL_FILE":r"ORG_BAK/0013_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T13_C =          {
                            "CLUT_FILE":r"ORG_BAK/0013_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T14_P = {
                            "PXL_FILE":r"ORG_BAK/0014_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":208,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T14_C =          {
                            "CLUT_FILE":r"ORG_BAK/0014_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ST57T15_P = {
                            "PXL_FILE":r"ORG_BAK/0015_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T15_C =          {
                            "CLUT_FILE":r"ORG_BAK/0015_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ST57T16_P = {
                            "PXL_FILE":r"ORG_BAK/0016_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":208,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T16_C =          {
                            "CLUT_FILE":r"ORG_BAK/0016_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T17_P = {
                            "PXL_FILE":r"ORG_BAK/0017_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":208,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T17_C =          {
                            "CLUT_FILE":r"ORG_BAK/0017_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T18_P = {
                            "PXL_FILE":r"ORG_BAK/0018_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":208,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T18_C =          {
                            "CLUT_FILE":r"ORG_BAK/0018_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T19_P = {
                            "PXL_FILE":r"ORG_BAK/0019_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":208,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T19_C =          {
                            "CLUT_FILE":r"ORG_BAK/0019_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ST57T20_P = {
                            "PXL_FILE":r"ORG_BAK/0020_ST57T.PIX",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":208,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST57T20_C =          {
                            "CLUT_FILE":r"ORG_BAK/0020_ST57T.PIX",
                            "CLUT_OFFSET":0*0x20,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
ImageHill.convertImage(ST57T4_P, ST57T4_C, "BMP/staff/0004_ST57T.PNG", False)
ImageHill.convertImage(ST57T5_P, ST57T5_C, "BMP/staff/0005_ST57T.PNG", False)
ImageHill.convertImage(ST57T6_P, ST57T6_C, "BMP/staff/0006_ST57T.PNG", False)
ImageHill.convertImage(ST57T7_P, ST57T7_C, "BMP/staff/0007_ST57T.PNG", False)
ImageHill.convertImage(ST57T8_P, ST57T8_C, "BMP/staff/0008_ST57T.PNG", False)
ImageHill.convertImage(ST57T9_P, ST57T9_C, "BMP/staff/0009_ST57T.PNG", False)
ImageHill.convertImage(ST57T10_P, ST57T10_C, "BMP/staff/0010_ST57T.PNG", False)
ImageHill.convertImage(ST57T11_P, ST57T11_C, "BMP/staff/0011_ST57T.PNG", False)
ImageHill.convertImage(ST57T12_P, ST57T12_C, "BMP/staff/0012_ST57T.PNG", False)
ImageHill.convertImage(ST57T13_P, ST57T13_C, "BMP/staff/0013_ST57T.PNG", False)
ImageHill.convertImage(ST57T14_P, ST57T14_C, "BMP/staff/0014_ST57T.PNG", False)
ImageHill.convertImage(ST57T15_P, ST57T15_C, "BMP/staff/0015_ST57T.PNG", False)
ImageHill.convertImage(ST57T16_P, ST57T16_C, "BMP/staff/0016_ST57T.PNG", False)
ImageHill.convertImage(ST57T17_P, ST57T17_C, "BMP/staff/0017_ST57T.PNG", False)
ImageHill.convertImage(ST57T18_P, ST57T18_C, "BMP/staff/0018_ST57T.PNG", False)
ImageHill.convertImage(ST57T19_P, ST57T19_C, "BMP/staff/0019_ST57T.PNG", False)
ImageHill.convertImage(ST57T20_P, ST57T20_C, "BMP/staff/0020_ST57T.PNG", False)
