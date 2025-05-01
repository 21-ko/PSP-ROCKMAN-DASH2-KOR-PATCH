from PIL import Image

MAP_FILE = 'DATA/fonts.utf8'
MAP_FONT = 'DATA/fonts.png'
DRAW_TXT = 'DATA/chars.txt'

def get_char_image(fonts_image, index, char_size=12, columns=20):
    x = (index % columns) * char_size
    y = (index // columns) * char_size
    return fonts_image.crop((x, y, x + char_size, y + char_size))

def makeimg():
    CHAR_SIZE = 12
    FONTS_PNG_COLUMNS = 20  # fonts에 한 줄에 배치된 글자 수
    START_NUM = 0  # 1번째부터
    START_X = START_NUM * CHAR_SIZE
    START_Y = CHAR_SIZE * 0  # 1번째 라인부터
    MAX_LINE_LENGTH = 41
    SPLIT_POSITION = 1722  # 1722번째 문자부터 img2에 작성
    
    with open(MAP_FILE, 'r', encoding='utf-8') as f:
        font_chars = f.read().replace('\n', '')
    fonts_image = Image.open(MAP_FONT).convert('RGBA')
    char_images = {char: get_char_image(fonts_image, index, CHAR_SIZE, FONTS_PNG_COLUMNS) 
                   for index, char in enumerate(font_chars)}
    
    with open(DRAW_TXT, 'r', encoding='utf-8') as f:
        draw_text = f.read().strip()
    
    img1 = Image.new('RGBA', (1024, 512), (0, 0, 0, 0))
    img2 = Image.new('RGBA', (1024, 512), (0, 0, 0, 0))
    
    # img1에 1~1721번째 글자 쓰기
    x1, y1 = START_X, START_Y
    char_count1 = START_NUM
    
    # img2에 1722번째 글자부터 쓰기
    x2, y2 = START_X, START_Y
    char_count2 = START_NUM
    
    for i, char in enumerate(draw_text):
        if char in char_images:
            if i < SPLIT_POSITION:
                # img1에 글자 쓰기
                img1.paste(char_images[char], (x1, y1), char_images[char])
                x1 += CHAR_SIZE
                char_count1 += 1
                if char_count1 >= MAX_LINE_LENGTH:
                    x1 = 0
                    y1 += CHAR_SIZE
                    char_count1 = 0
            else:
                # img2에 글자 쓰기
                img2.paste(char_images[char], (x2, y2), char_images[char])
                x2 += CHAR_SIZE
                char_count2 += 1
                if char_count2 >= MAX_LINE_LENGTH:
                    x2 = 0
                    y2 += CHAR_SIZE
                    char_count2 = 0
    
    img1.save('DATA/font1.png')
    img2.save('DATA/font2.png')
    
makeimg()