#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv) {
	setuid(0);

	char** args = malloc(sizeof(char*) * (argc + 2));
	args[argc] = 0;
	args[0] = "/usr/local/bin/python";
	args[1] = "rmain.py";
	for(int i = 1; i < argc; ++i)
		args[i + 1] = argv[i];

	execvp(args[0], args);
	return 0;
}
