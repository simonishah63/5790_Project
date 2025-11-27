# CBMC container (multi-arch, runs natively on ARM64)
FROM --platform=linux/amd64 diffblue/cbmc:latest

WORKDIR /workspace

ENTRYPOINT ["/usr/bin/bin/cbmc"]
