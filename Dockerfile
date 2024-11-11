FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    wget \
    tar \
    hdf5-tools \
    h5utils \
    libhdf5-dev \
    bzip2 \
    libbz2-dev \
    liblzma-dev \
    unzip \
    pipx

ADD radiantkit /root/radiantkit/radiantkit
ADD pyproject.toml /root/radiantkit/
RUN pipx install /root/radiantkit/

RUN pipx ensurepath
ENV PATH="./root/.local/bin/:$PATH"

CMD [ "/bin/bash" ]
