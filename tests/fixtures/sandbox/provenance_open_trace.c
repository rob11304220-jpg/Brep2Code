#define _GNU_SOURCE

#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void log_input_access(const char *path) {
    const char *trace = getenv("BREP2CODE_PROVENANCE_TRACE");
    if (trace == NULL || path == NULL || strstr(path, "model.step") == NULL) {
        return;
    }
    FILE *file = fopen(trace, "a");
    if (file != NULL) {
        fprintf(file, "pid=%ld path=%s\n", (long)getpid(), path);
        fclose(file);
    }
}

int open(const char *path, int flags, ...) {
    static int (*real_open)(const char *, int, ...) = NULL;
    mode_t mode = 0;
    if (real_open == NULL) real_open = dlsym(RTLD_NEXT, "open");
    if (flags & O_CREAT) {
        va_list args;
        va_start(args, flags);
        mode = va_arg(args, mode_t);
        va_end(args);
        log_input_access(path);
        return real_open(path, flags, mode);
    }
    log_input_access(path);
    return real_open(path, flags);
}

int openat(int dirfd, const char *path, int flags, ...) {
    static int (*real_openat)(int, const char *, int, ...) = NULL;
    mode_t mode = 0;
    if (real_openat == NULL) real_openat = dlsym(RTLD_NEXT, "openat");
    if (flags & O_CREAT) {
        va_list args;
        va_start(args, flags);
        mode = va_arg(args, mode_t);
        va_end(args);
        log_input_access(path);
        return real_openat(dirfd, path, flags, mode);
    }
    log_input_access(path);
    return real_openat(dirfd, path, flags);
}

int open64(const char *path, int flags, ...) {
    static int (*real_open64)(const char *, int, ...) = NULL;
    mode_t mode = 0;
    if (real_open64 == NULL) real_open64 = dlsym(RTLD_NEXT, "open64");
    if (flags & O_CREAT) {
        va_list args;
        va_start(args, flags);
        mode = va_arg(args, mode_t);
        va_end(args);
        log_input_access(path);
        return real_open64(path, flags, mode);
    }
    log_input_access(path);
    return real_open64(path, flags);
}

int openat64(int dirfd, const char *path, int flags, ...) {
    static int (*real_openat64)(int, const char *, int, ...) = NULL;
    mode_t mode = 0;
    if (real_openat64 == NULL) real_openat64 = dlsym(RTLD_NEXT, "openat64");
    if (flags & O_CREAT) {
        va_list args;
        va_start(args, flags);
        mode = va_arg(args, mode_t);
        va_end(args);
        log_input_access(path);
        return real_openat64(dirfd, path, flags, mode);
    }
    log_input_access(path);
    return real_openat64(dirfd, path, flags);
}

FILE *fopen(const char *path, const char *mode) {
    static FILE *(*real_fopen)(const char *, const char *) = NULL;
    if (real_fopen == NULL) real_fopen = dlsym(RTLD_NEXT, "fopen");
    log_input_access(path);
    return real_fopen(path, mode);
}

FILE *fopen64(const char *path, const char *mode) {
    static FILE *(*real_fopen64)(const char *, const char *) = NULL;
    if (real_fopen64 == NULL) real_fopen64 = dlsym(RTLD_NEXT, "fopen64");
    log_input_access(path);
    return real_fopen64(path, mode);
}
