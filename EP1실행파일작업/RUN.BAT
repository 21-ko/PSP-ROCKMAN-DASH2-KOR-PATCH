:: asm 패치
armips EXE\patch.s

:: 한글 테이블 생성
python TOOLS\maketbl.py

:: 자막 조정
python TOOLS\editpostags.py

:: 자막 삽입
python TOOLS\txt2bin.py EBOOT

:: 테이블 업데이트
copy /Y .\Moji.tbl ..\EP1\MojiKor.tbl

:: 삭제
rmdir /s /q ".\EBOOT"
del .\Moji.tbl

pause