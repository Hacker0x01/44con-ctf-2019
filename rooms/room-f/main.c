#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

uint32_t crc32_for_byte(uint32_t r) {
  for(int j = 0; j < 8; ++j)
    r = (r & 1? 0: (uint32_t)0xEDB88320L) ^ r >> 1;
  return r ^ (uint32_t) 0xFF000000L;
}

void crc32(const void *data, size_t n_bytes, uint32_t* crc) {
  static uint32_t table[0x100];
  if(!*table)
    for(size_t i = 0; i < 0x100; ++i)
      table[i] = crc32_for_byte(i);
  for(size_t i = 0; i < n_bytes; ++i)
    *crc = table[(uint8_t)*crc ^ ((uint8_t*)data)[i]] ^ *crc >> 8;
}

int main(int argc, char **argv) {
	setuid(0);

	char buf[100];
	printf("%p\n", (void*) main);
	printf("%p\n", (void*) buf);
	sleep(3);
	FILE* fp = fopen("message", "rb");
	fseek(fp, 0L, SEEK_END);
	long len = ftell(fp) - 4;
	fseek(fp, 0L, SEEK_SET);
	uint32_t check;
	fread(&check, 4, 1, fp);
	fread(buf, 1, len, fp);
	buf[len] = 0;

	uint32_t real = 0;
	crc32(buf, len, &real);
	if(real != check)
		memset(buf, 0, len);
	else
		puts(buf);

	return 0;
}
