#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv) {
	if(argc < 2) {
		printf("./main [name]\n");
		return 1;
	}
	setuid(0);
	char *buf = (char*) malloc(strlen(argv[1]) + 1000);
	sprintf(buf, "echo C\\'mon %s. Show me what you\\'re made of.", argv[1]);
	system(buf);
	return 0;
}
