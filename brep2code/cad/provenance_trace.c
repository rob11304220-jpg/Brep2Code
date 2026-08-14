#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static void attest_coverage(void) __attribute__((constructor));

static void attest_coverage(void) {
    const char *trace = getenv("BREP2CODE_PROVENANCE_TRACE");
    if (trace == NULL) return;
    int fd = syscall(SYS_openat, AT_FDCWD, trace, O_WRONLY | O_CREAT | O_APPEND, 0600);
    if (fd >= 0) {
        if (write(fd, "coverage=active\n", 16) < 0) {
            (void)close(fd);
            return;
        }
        (void)close(fd);
    }
}

static void trace_input(const char *path) {
    const char *trace = getenv("BREP2CODE_PROVENANCE_TRACE");
    if (trace == NULL || path == NULL || strncmp(path, "/input/", 7) != 0) return;
    FILE *file = fopen(trace, "a");
    if (file != NULL) { fprintf(file, "pid=%ld path=%s\n", (long)getpid(), path); fclose(file); }
}

int open(const char *path, int flags, ...) {
    static int (*real)(const char *, int, ...) = NULL; if (!real) real = dlsym(RTLD_NEXT, "open");
    va_list args; va_start(args, flags); mode_t mode = (flags & O_CREAT) ? va_arg(args, mode_t) : 0; va_end(args);
    trace_input(path); return (flags & O_CREAT) ? real(path, flags, mode) : real(path, flags);
}
int open64(const char *path, int flags, ...) {
    static int (*real)(const char *, int, ...) = NULL; if (!real) real = dlsym(RTLD_NEXT, "open64");
    va_list args; va_start(args, flags); mode_t mode = (flags & O_CREAT) ? va_arg(args, mode_t) : 0; va_end(args);
    trace_input(path); return (flags & O_CREAT) ? real(path, flags, mode) : real(path, flags);
}
int openat(int fd, const char *path, int flags, ...) {
    static int (*real)(int, const char *, int, ...) = NULL; if (!real) real = dlsym(RTLD_NEXT, "openat");
    va_list args; va_start(args, flags); mode_t mode = (flags & O_CREAT) ? va_arg(args, mode_t) : 0; va_end(args);
    trace_input(path); return (flags & O_CREAT) ? real(fd, path, flags, mode) : real(fd, path, flags);
}
int openat64(int fd, const char *path, int flags, ...) {
    static int (*real)(int, const char *, int, ...) = NULL; if (!real) real = dlsym(RTLD_NEXT, "openat64");
    va_list args; va_start(args, flags); mode_t mode = (flags & O_CREAT) ? va_arg(args, mode_t) : 0; va_end(args);
    trace_input(path); return (flags & O_CREAT) ? real(fd, path, flags, mode) : real(fd, path, flags);
}
FILE *fopen(const char *path, const char *mode) {
    static FILE *(*real)(const char *, const char *) = NULL; if (!real) real = dlsym(RTLD_NEXT, "fopen"); trace_input(path); return real(path, mode);
}
FILE *fopen64(const char *path, const char *mode) {
    static FILE *(*real)(const char *, const char *) = NULL; if (!real) real = dlsym(RTLD_NEXT, "fopen64"); trace_input(path); return real(path, mode);
}
