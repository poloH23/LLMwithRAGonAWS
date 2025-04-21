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

## Copy the Conda environment file
#COPY bak/environment.yml .
#ARG ENV_NAME=atap
#ENV ENV_NAME=${ENV_NAME}
#
## Set project directory
#WORKDIR /app
#RUN conda install -n base -c conda-forge mamba
#
## Create a conda environment (named base, using Python 3.9.19
#RUN conda update -n base -c defaults conda
#COPY bak/environment.yml .
#RUN mamba env create -f environment.yml
#RUN conda clean -afy

## Copy the entire project (customizable)
#COPY . .


# Preset execution
#SHELL ["conda", "run", "-n", "atap", "/bin/bash", "-c"]

#Default execution (will execute make command)
#CMD ["make", "docker-run"]

# Dockerfile
#FROM python:3.10-slim

# Setting UTF-8
#ENV PYTHONUNBUFFERED=1 \
#    LANG=C.UTF-8 \
#    LC_ALL=C.UTF-8

# Set working diretory
#WORKDIR /app

# install system dependnencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    curl \
#    && rm -rf /var/lib/apt/lists/*

# Copy requirements
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (customizable)
#COPY . .

# Preset execution: can be overridden by docker-compose
#CMD ["python", "main/__init__.py"]
