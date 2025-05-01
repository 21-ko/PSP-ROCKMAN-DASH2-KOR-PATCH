#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc != 5) {
        fprintf(stderr, "����: %s ������ ũ�� ���� �������\n", argv[0]);
        return 1;
    }

    long offset = strtol(argv[1], NULL, 0);
    long size   = strtol(argv[2], NULL, 0);
    const char* input_path  = argv[3];
    const char* output_path = argv[4];

    FILE* in = fopen(input_path, "rb");
    if (!in) {
        perror("�Է� ���� ���� ����");
        return 1;
    }

    FILE* out = fopen(output_path, "wb");
    if (!out) {
        perror("��� ���� ���� ����");
        fclose(in);
        return 1;
    }

    if (fseek(in, offset, SEEK_SET) != 0) {
        perror("������ �̵� ����");
        fclose(in);
        fclose(out);
        return 1;
    }

    char* buffer = malloc(size);
    if (!buffer) {
        fprintf(stderr, "�޸� �Ҵ� ����\n");
        fclose(in);
        fclose(out);
        return 1;
    }

    size_t read_bytes = fread(buffer, 1, size, in);
    if (read_bytes != size) {
        fprintf(stderr, "���� ũ�� ����ġ: %zu ����Ʈ\n", read_bytes);
    }

    fwrite(buffer, 1, read_bytes, out);

    free(buffer);
    fclose(in);
    fclose(out);

    printf("���Ͽ��� %ld ����Ʈ @ 0x%lX ���� �Ϸ�: %s\n", read_bytes, offset, output_path);
    return 0;
}
