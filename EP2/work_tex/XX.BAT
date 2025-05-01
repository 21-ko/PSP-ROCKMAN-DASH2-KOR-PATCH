set source_folder=ORG_BAK
set destination_folder=ORG
xcopy "%source_folder%\*" "%destination_folder%\" /s /e /h /y

python XxTex.py

call æ–√‡.bat
pause