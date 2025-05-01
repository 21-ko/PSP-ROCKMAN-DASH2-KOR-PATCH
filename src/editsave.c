#include <stdio.h>
#include <stdint.h>

#define FILE_NAME       "DATA.BIN.DEC"
#define WORD_SIZE       2
#define REPEAT_COUNT    3

#define TARGET_VALUE    0xF818
#define REPLACE_VALUE   0x005B

#define PATCH_BYTES      { 0x06, 0xF4, 0x0F, 0xF5, 0x4C, 0x00 }

#define WRITE_PATCH(fp, offset)                       \
    do {                                              \
        uint8_t patch[6] = PATCH_BYTES;               \
        fseek((fp), (offset), SEEK_SET);              \
        fwrite(patch, 1, 6, (fp));                    \
    } while (0)

#define READ_LE_WORD(fp, offset, out_value_ptr)        \
    do {                                               \
        uint8_t _buf[2];                               \
        fseek((fp), (offset), SEEK_SET);               \
        fread(_buf, 1, 2, (fp));                       \
        *(out_value_ptr) = _buf[0] | (_buf[1] << 8);   \
    } while (0)

#define WRITE_LE_WORD(fp, offset, value)               \
    do {                                               \
        uint8_t _buf[2];                               \
        _buf[0] = (value) & 0xFF;                      \
        _buf[1] = ((value) >> 8) & 0xFF;               \
        fseek((fp), (offset), SEEK_SET);               \
        fwrite(_buf, 1, 2, (fp));                      \
    } while (0)

#define CHECK_AND_REPLACE(fp, offset)                  \
    do {                                               \
        uint16_t _val;                                 \
        READ_LE_WORD((fp), (offset), &_val);           \
        if (_val == TARGET_VALUE) {                    \
            WRITE_LE_WORD((fp), (offset), REPLACE_VALUE); \
        }                                              \
    } while (0)

int main() {
    FILE *fp = fopen(FILE_NAME, "r+b");
    if (!fp) {
        perror("파일 열기 실패");
        return 1;
    }

    WRITE_PATCH(fp, 0xB34);
    WRITE_PATCH(fp, 0xB58);
    WRITE_PATCH(fp, 0xB7C);

    long base_offsets[] = {0xB40, 0xB4C, 0xB64, 0xB70, 0xB88, 0xB94};

    for (size_t i = 0; i < 7; ++i) {
        for (int j = 0; j < REPEAT_COUNT; ++j) {
            long curr_offset = base_offsets[i] + (j * WORD_SIZE);
            CHECK_AND_REPLACE(fp, curr_offset);
        }
    }

    fclose(fp);
    return 0;
}
