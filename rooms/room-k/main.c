#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static uint64_t globals[256];
static int spos = 127;
static int pos = 0;
static FILE* fp;
static long len;
static uint8_t* buf;

void sub() {
	uint64_t stack[128];
	memset(stack, 0, 128 * 8);
	fp = fopen("code.bin", "rb");
	fseek(fp, 0L, SEEK_END);
	len = ftell(fp);
	fseek(fp, 0L, SEEK_SET);
	buf = malloc(len);
	fread(buf, 1, len, fp);

	while(1) {
		switch(buf[pos]) {
			case 0:
				return;
			case 1:
				globals[buf[pos + 1]] = stack[spos++];
				pos++;
				break;
			case 2:
				stack[--spos] = globals[buf[pos + 1]];
				pos++;
				break;
			case 3:
				stack[spos - 1] = stack[spos];
				spos--;
				break;
			case 4:
				stack[spos - 1] = *(uint64_t*) stack[spos];
				spos--;
				break;
			case 5:
				stack[--spos] = *(uint64_t*) (buf + pos + 1);
				pos += 8;
				break;
			case 6: {
				uint64_t temp = stack[spos + 1];
				stack[spos + 1] = stack[spos];
				stack[spos] = temp;
				break;
			}
			case 7: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = a + b;
				break;
			}
			case 8: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = a - b;
				break;
			}
			case 9: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = a & b;
				break;
			}
			case 10: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = a | b;
				break;
			}
			case 11: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = a << b;
				break;
			}
			case 12: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = a >> b;
				break;
			}
			case 13: {
				uint64_t a = stack[spos++];
				uint64_t b = stack[spos++];
				stack[--spos] = (uint64_t) (((int64_t) a) >> b);
				break;
			}
			case 14:
				printf("0x%llx\n", stack[spos++]);
				break;
			case 15:
				if(stack[spos++] != 0)
					pos = pos + *(int64_t*) (buf + pos + 1) - 1;
				else
					pos += 8;
				break;
		}
		pos++;
	}
}

int main(int argc, char **argv) {
	sub();
	return 0;
}
