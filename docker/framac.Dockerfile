# Frama-C 25 container (amd64 only)
FROM --platform=linux/amd64 framac/frama-c:25.0

WORKDIR /workspace

ENTRYPOINT ["frama-c"]
