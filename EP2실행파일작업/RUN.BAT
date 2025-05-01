:: asm 패치
armips EXE\patch.s

:: 폰트 생성
python TOOLS\draw.py
python TOOLS\png2vram.py
python TOOLS\maketbl.py

:: 폰트 삽입
python TOOLS\makeboot.py

:: 자막 조정
python TOOLS\editpostags.py

:: 자막 삽입
python TOOLS\txt2bin.py EBOOT

:: lba, size 업데이트
python TOOLS\editlba.py

:: 테이블 파일 업데이트
copy /Y .\Moji.tbl ..\Tools\MojiKor.tbl

:: 파일 삭제
del .\Moji.tbl
del DATA\font1.png
del DATA\font2.png
del DATA\VRAM.PIX
rmdir /s /q ".\EBOOT"

pause