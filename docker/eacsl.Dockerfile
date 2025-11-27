FROM framac/frama-c:25.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    make \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# E-ACSL is included with Frama-C, but we need to ensure it's properly set up
# Create a wrapper script for E-ACSL
RUN echo '#!/bin/bash\nframa-c -e-acsl "$@"' > /usr/local/bin/e-acsl-gcc.sh && \
    chmod +x /usr/local/bin/e-acsl-gcc.sh

WORKDIR /workspace

CMD ["/bin/bash"]