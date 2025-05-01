set source_folder=DAT_ORG
set destination_folder=DAT
xcopy "%source_folder%\*" "%destination_folder%\" /s /e /h /y

python txt2msg.py XMessKor\ST07-0x00012000.TXT
python txt2msg.py XMessKor\ST20-0x00014800.TXT
python txt2msg.py XMessKor\ST2001-0x00014800.TXT
python txt2msg.py XMessKor\ST21-0x0000e000.TXT
python txt2msg.py XMessKor\ST22-0x00018800.TXT
python txt2msg.py XMessKor\ST23-0x0001d000.TXT
python txt2msg.py XMessKor\ST24-0x00026800.TXT
python txt2msg.py XMessKor\ST26-0x00014800.TXT
python txt2msg.py XMessKor\ST27T-0x00002000.TXT
python txt2msg.py XMessKor\ST28-0x00014000.TXT
python txt2msg.py XMessKor\ST29-0x0000c800.TXT
pause