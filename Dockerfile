# Using miniconda base image
FROM continuumio/miniconda3

# Set project directory
WORKDIR /workspace

# Install 'make' package and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gawk \
    make \
    git \
    curl \
    ca-certificates \
    && pip install pre-commit \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project (customizable)
COPY . .

# Default execution (shell)
CMD ["/bin/bash"]
