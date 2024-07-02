FROM mambaorg/micromamba:1.5.8
USER root
COPY backend/environment-prod.yml /tmp/env.yml
RUN micromamba install -y -n base -f /tmp/env.yml && \
    micromamba clean --all --yes
RUN apt update && apt install -y make
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN mkdir -p /common_processing/src/common_processing && \
  touch /common_processing/src/common_processing/__init__.py
COPY common_processing/setup.cfg \
  common_processing/setup.py \
  /common_processing/
RUN python -m pip install -e /common_processing
WORKDIR /app
