#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc != 5) {
        fprintf(stderr, "사용법: %s 오프셋 크기 파일 출력파일\n", argv[0]);
        return 1;
    }

    long offset = strtol(argv[1], NULL, 0);
    long size   = strtol(argv[2], NULL, 0);
    const char* input_path  = argv[3];
    const char* output_path = argv[4];

    FILE* in = fopen(input_path, "rb");
    if (!in) {
        perror("입력 파일 열기 실패");
        return 1;
    }

    FILE* out = fopen(output_path, "wb");
    if (!out) {
        perror("출력 파일 생성 실패");
        fclose(in);
        return 1;
    }

    if (fseek(in, offset, SEEK_SET) != 0) {
        perror("오프셋 이동 실패");
        fclose(in);
        fclose(out);
        return 1;
    }

    char* buffer = malloc(size);
    if (!buffer) {
        fprintf(stderr, "메모리 할당 실패\n");
        fclose(in);
        fclose(out);
        return 1;
    }

    size_t read_bytes = fread(buffer, 1, size, in);
    if (read_bytes != size) {
        fprintf(stderr, "읽은 크기 불일치: %zu 바이트\n", read_bytes);
    }

    fwrite(buffer, 1, read_bytes, out);

    free(buffer);
    fclose(in);
    fclose(out);

    printf("파일에서 %ld 바이트 @ 0x%lX 추출 완료: %s\n", read_bytes, offset, output_path);
    return 0;
}
