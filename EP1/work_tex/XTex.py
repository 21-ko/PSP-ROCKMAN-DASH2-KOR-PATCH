import ImageHill
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil

def CropImg(image_path, x, y, w, h):
    img = Image.open(image_path)
    cropped_img = img.crop((x, y, x + w, y + h))
    return cropped_img

# SUBSCN
subscC =          {
                            "CLUT_FILE":r"ORG/GAME-0x00030800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

SUBSCN06_P = {
                            "PXL_FILE":r"ORG/SUBSCN06-0x00000000-2.bin",
                            "PXL_OFFSET":0x800-0x30,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

SUBSCN03_P = {
                            "PXL_FILE":r"ORG/SUBSCN03-0x00001800-2.bin",
                            "PXL_OFFSET":0x800-0x30,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

SUBSCN04_P = {
                            "PXL_FILE":r"ORG/SUBSCN04-0x00000000-2.bin",
                            "PXL_OFFSET":0x800-0x30,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

# GAME
GAME_C =      {
                            "CLUT_FILE":r"ORG/GAME-0x00030800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

GAME_P = {
                            "PXL_FILE":r"ORG/GAME-0x00030800-3.uncomp.bin",
                            "PXL_OFFSET":0x100,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }

# ST23T
ST23T1_C =          {
                            "CLUT_FILE":r"ORG/ST23T-0x00041000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

ST23T1_P = {
                            "PXL_FILE":r"ORG/ST23T-0x00041000-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST23T2_C =    {
                            "CLUT_FILE":r"ORG/ST23T-0x00043800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ST23T2_P = {
                            "PXL_FILE":r"ORG/ST23T-0x00043800-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST23T3_C =    {
                            "CLUT_FILE":r"ORG/ST23T-0x00046800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

ST23T3_P = {
                            "PXL_FILE":r"ORG/ST23T-0x00046800-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }


# ST25T
ST25T_C =          {
                            "CLUT_FILE":r"ORG/ST25T-0x00049000-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

ST25T_P = {
                            "PXL_FILE":r"ORG/ST25T-0x00049000-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
ST25T2_C =          {
                            "CLUT_FILE":r"ORG/ST25T-0x0004d800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
    
    
                        }

ST25T2_P = {
                            "PXL_FILE":r"ORG/ST25T-0x0004d800-3.uncomp.bin",
                            "PXL_OFFSET":0x80,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
                        
# TITLE
TITLE_C =          {
                            "CLUT_FILE":r"ORG/TITLE-0x00005800-3.uncomp.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }

TITLE_P = {
                            "PXL_FILE":r"ORG/TITLE-0x00005800-3.uncomp.bin",
                            "PXL_OFFSET":0x200,
                            "WIDTH":544,
                            "HEIGHT":60,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE2_P = {
                            "PXL_FILE":r"ORG/TITLE-0x00008000-3.uncomp.bin",
                            "PXL_OFFSET":0,
                            "WIDTH":544,
                            "HEIGHT":60,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE3_P = {
                            "PXL_FILE":r"ORG/TITLE-0x0000b000-3.uncomp.bin",
                            "PXL_OFFSET":0,
                            "WIDTH":544,
                            "HEIGHT":60,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }
                        
TITLE4_P = {
                            "PXL_FILE":r"ORG/TITLE-0x0000d800-3.uncomp.bin",
                            "PXL_OFFSET":0,
                            "WIDTH":544,
                            "HEIGHT":60,
                            "PXL_MODE":ImageHill.EIGHT_BIT
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
                        
TITLE5_P = {
                            "PXL_FILE":r"ORG/TITLE-0x0000f800-3.uncomp.bin",
                            "PXL_OFFSET":0xC0,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
                        
# SELECT
SELECT_C =          {
                            "CLUT_FILE":r"ORG/SELECT-0x00003800-2.bin",
                            "CLUT_OFFSET":0,
                            "N_COLORS":0x10,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
SELECT_P = {
                            "PXL_FILE":r"ORG/SELECT-0x00000000-3.uncomp.bin",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
SELECT2_P = {
                            "PXL_FILE":r"ORG/SELECT-0x00004800-3.uncomp.bin",
                            "PXL_OFFSET":0x20,
                            "WIDTH":256,
                            "HEIGHT":256,
                            "PXL_MODE":ImageHill.FOUR_BIT
                        }
                        
SELECT3_C =  {
                            "CLUT_FILE":r"ORG/SELECT-0x0001c800-3.uncomp.bin",
                            "CLUT_OFFSET":0x0,
                            "N_COLORS":0x100,
                            "CLUT_MODE":ImageHill.RGBA_5551_PS1
                        }
                        
SELECT3_P = {
                            "PXL_FILE":r"ORG/SELECT-0x0001c800-3.uncomp.bin",
                            "PXL_OFFSET":0x200,
                            "WIDTH":256,
                            "HEIGHT":128,
                            "PXL_INSET":0,
                            "PXL_MODE":ImageHill.EIGHT_BIT
                        }


ImageHill.convertImage(SUBSCN06_P, subscC, "BMP/SUBSCN06-0x00000000-2.png", False)
ImageHill.convertImage(SUBSCN03_P, subscC, "BMP/SUBSCN03-0x00001800-2.png", False)
ImageHill.convertImage(SUBSCN04_P, subscC, "BMP/SUBSCN04-0x00000000-2.png", False)

ImageHill.convertImage(GAME_P, GAME_C, "BMP/GAME-0x00030800-3.uncomp.png", False)

ImageHill.convertImage(ST23T1_P, ST23T1_C, "BMP/ST23T-0x00041000-3.uncomp.png", False)
ImageHill.convertImage(ST23T2_P, ST23T2_C, "BMP/ST23T-0x00043800-3.uncomp.png", False)
ImageHill.convertImage(ST23T3_P, ST23T3_C, "BMP/ST23T-0x00046800-3.uncomp.png", False)

ImageHill.convertImage(ST25T_P, ST25T_C, "BMP/ST25T-0x00049000-3.uncomp.png", False)
ImageHill.convertImage(ST25T2_P, ST25T2_C, "BMP/ST25T-0x0004d800-3.uncomp.png", False)

ImageHill.convertImage(TITLE_P, TITLE_C, "BMP/TITLE/TITLE-0x00005800-3.uncomp.png", False)
ImageHill.convertImage(TITLE2_P, TITLE_C, "BMP/TITLE/TITLE-0x00008000-3.uncomp.png", False)
ImageHill.convertImage(TITLE3_P, TITLE_C, "BMP/TITLE/TITLE-0x0000b000-3.uncomp.png", False)
ImageHill.convertImage(TITLE4_P, TITLE_C, "BMP/TITLE/TITLE-0x0000d800-3.uncomp.png", False)

# TITLE5
os.makedirs("./BMP/TEMP", exist_ok=True) # 임시 폴더 생성
ImageHill.convertImage(TITLE5_P, TITLE5_0_C, "BMP/TEMP/TITLE-0x0000f800-3.uncomp_0.png", False)
ImageHill.convertImage(TITLE5_P, TITLE5_1_C, "BMP/TEMP/TITLE-0x0000f800-3.uncomp_1.png", False)
ImageHill.convertImage(TITLE5_P, TITLE5_2_C, "BMP/TEMP/TITLE-0x0000f800-3.uncomp_2.png", False)
# 자르기
img1 = CropImg("BMP/TEMP/TITLE-0x0000f800-3.uncomp_0.png", 0, 0, 208, 40)
img2 = CropImg("BMP/TEMP/TITLE-0x0000f800-3.uncomp_1.png", 0, 40, 208, 80)
img3 = CropImg("BMP/TEMP/TITLE-0x0000f800-3.uncomp_2.png", 0, 120, 208, 136)
img4 = CropImg("BMP/TEMP/TITLE-0x0000f800-3.uncomp_1.png", 208, 0, 48, 256)
# 결합
final_img = Image.new('RGBA', (256, 256))
final_img.paste(img1, (0, 0))
final_img.paste(img2, (0, 40))
final_img.paste(img3, (0, 120))
final_img.paste(img4, (208, 0))
final_img.save("BMP/TITLE-0x0000f800-3.uncomp.png")
# 폴더 삭제
shutil.rmtree("./BMP/TEMP")


ImageHill.convertImage(SELECT_P, SELECT_C, "BMP/SELECT-0x00000000-3.uncomp.png", False)
ImageHill.convertImage(SELECT2_P, SELECT_C, "BMP/SELECT-0x00004800-3.uncomp.png", False)

ImageHill.convertImage(SELECT3_P, SELECT3_C, "BMP/SELECT-0x0001c800-3.uncomp.png", False)