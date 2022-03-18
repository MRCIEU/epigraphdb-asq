FROM continuumio/miniconda3:4.10.3
RUN apt update && apt install -y make
COPY backend/environment.yml ./
RUN conda env create -f environment.yml
RUN echo "conda activate asq-api" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
ENV PATH /opt/conda/envs/asq-api/bin:$PATH
WORKDIR /app
RUN mkdir -p /common_processing/src/common_processing && \
  touch /common_processing/src/common_processing/__init__.py
COPY common_processing/setup.cfg \
  common_processing/setup.py \
  /common_processing/
RUN /opt/conda/envs/asq-api/bin/python -m pip install -e /common_processing
