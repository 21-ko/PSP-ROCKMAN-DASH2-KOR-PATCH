# 출처: https://github.com/HilltopWorks/Mega-Man-Legends-2-Demo/blob/main/filesys.py

import os
from pathlib import Path
import sys

def unpack_all():
    os.makedirs("unpack\\DAT", exist_ok=True)
    
    files = Path("DAT").glob('*.bin')
    for file in files:
        out_folder =  "unpack\\DAT\\"
        unpack_file(file, os.path.join(out_folder, Path(file).stem))
    
    return

unpack_all()
