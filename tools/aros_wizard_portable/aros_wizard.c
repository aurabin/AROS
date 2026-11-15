/* Portable AROS Wizard CLI: no privileged operations. */
#include "wizard_core.h"
#include <stdio.h>
#include <string.h>
static void help(void) {
    puts("AROS Wizard portable 0.2.0-dev\n"
         "Usage: aros-wizard [--help|--version|--platform|--diagnose|--check-path FILE]\n"
         "Read-only host diagnostics and image file inspection (no installation).");
}
int main(int argc, char **argv) {
    if (argc == 1 || (argc == 2 && strcmp(argv[1], "--help") == 0)) { help(); return 0; }
    if (argc == 2 && strcmp(argv[1], "--version") == 0) { puts("0.2.0-dev"); return 0; }
    if (argc == 2 && strcmp(argv[1], "--platform") == 0) { puts(wizard_platform()); return 0; }
    if (argc == 2 && strcmp(argv[1], "--diagnose") == 0) {
        printf("Host: %s\nMode: read-only\nAROS installer: unavailable\n", wizard_platform());
        return 0;
    }
    if (argc == 3 && strcmp(argv[1], "--check-path") == 0) {
        unsigned long long size = 0;
        if (!wizard_file_size(argv[2], &size)) {
            fprintf(stderr, "Cannot open regular image file: %s\n", argv[2]); return 1;
        }
        printf("Readable file: %s\nSize: %llu bytes\nImage validity: not verified\n", argv[2], size);
        return 0;
    }
    fprintf(stderr, "Invalid arguments; use --help\n");
    return 2;
}
