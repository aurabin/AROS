#ifndef AROS_WIZARD_CORE_H
#define AROS_WIZARD_CORE_H
const char *wizard_platform(void);
/* Returns 1 only for readable regular files; does not validate ISO contents. */
int wizard_file_size(const char *path, unsigned long long *size);
#endif
