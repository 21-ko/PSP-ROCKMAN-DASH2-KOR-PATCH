import struct

with open("DATA/lba.bin", "rb") as f:
    buffer = bytearray(f.read())

with open("DATA/lba.txt", "r", encoding="utf-8") as f:
    offset = 0

    for line in f:
        parts = line.strip().split(" , ")
        if len(parts) < 2:
            continue

        lba = int(parts[0])
        size = int(parts[1])

        struct.pack_into("<III", buffer, offset, 0, lba, size)
        offset += 12

with open("EBOOT.BIN", "r+b") as f:
    f.seek(0x4E2D00)
    f.write(buffer)

