#!/bin/sh

# Build for docker
# gcc r.c -o ezorange -no-pie


# Build for local & publish
gcc r.c -o ezorange -no-pie
patchelf --set-interpreter ./ld-2.32.so ezorange
patchelf --replace-needed libc.so.6 ./libc.so.6 ezorange