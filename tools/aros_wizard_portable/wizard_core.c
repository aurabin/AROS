#include "wizard_core.h"
#include <stdio.h>
#include <sys/stat.h>
#if defined(_WIN32)
#include <windows.h>
#endif
const char *wizard_platform(void) {
#if defined(__HAIKU__)
    return "Haiku";
#elif defined(__FreeBSD__)
    return "FreeBSD";
#elif defined(__OpenBSD__)
    return "OpenBSD";
#elif defined(__NetBSD__)
    return "NetBSD";
#elif defined(__DragonFly__)
    return "DragonFly BSD";
#elif defined(__linux__)
    return "Linux";
#elif defined(_WIN32)
    return "Windows/ReactOS (Win32)";
#else
    return "Unknown host";
#endif
}
int wizard_file_size(const char *path, unsigned long long *size) {
    FILE *fp;
    unsigned char buf[4096];
    size_t n;
    unsigned long long total = 0;
    struct stat st;
    if (!path || !*path || !size) return 0;
    if (stat(path, &st) != 0 || !(st.st_mode & S_IFREG)) return 0;
    fp = fopen(path, "rb");
    if (!fp) return 0;
    while ((n = fread(buf, 1, sizeof(buf), fp)) > 0) {
        if (total > (~0ULL) - (unsigned long long)n) { fclose(fp); return 0; }
        total += (unsigned long long)n;
    }
    if (ferror(fp) || fclose(fp) != 0) return 0;
    *size = total;
    return 1;
}
