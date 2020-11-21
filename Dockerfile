FROM ubuntu:18.04

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
                ca-certificates \
                netbase \
        && rm -rf /var/lib/apt/lists/*

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=manga
ARG HOST_GROUP=manga
ARG HOME='/home/manga'

RUN groupadd -g $HOST_GID $HOST_GROUP \
    && groupadd sudonopswd \
    && useradd -m -l -g $HOST_GROUP -u $HOST_UID $HOST_USER

RUN mkdir $HOME -p; \
    chown $HOST_USER:$HOST_GROUP $HOME

RUN touch $HOME/.bashrc; \
    mkdir $HOME/Manga; \
    chown $HOST_USER:$HOST_GROUP $HOME/.bashrc; \
    chown $HOST_USER:$HOST_GROUP $HOME/Manga

RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    libxml2-dev libxslt1-dev python3.7 python3-pip python3-lxml nodejs npm python3-argcomplete libjpeg-dev \
    zlib1g-dev libjpeg8-dev zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev libwebp-dev libopenjp2-7-dev

RUN python3 -m pip install pillow --global-option="build_ext" --global-option="--enable-zlib" \
    --global-option="--enable-jpeg" --global-option="--enable-tiff" --global-option="--enable-freetype" \
    --global-option="--enable-webp" --global-option="--enable-webpmux" --global-option="--enable-jpeg2000"

RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && DEBIAN_FRONTEND=noninteractive apt-get autoclean

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
    ; ln -s idle3 idle \
    ; ln -s pydoc3 pydoc \
    ; ln -s python3 python \
    ; ln -s python3-config python-config

RUN python3 -m pip install manga-py -U --no-cache-dir

RUN echo 'Manga-py version: '; \
    manga-py --version; \
    rm -rf /tmp/.P*

USER $HOST_USER
WORKDIR $HOME

# docker run -it -v /tmp/destination:/home/manga mangadl/manga-py

ENTRYPOINT  ["manga-py"]
CMD ["manga-py", "--version"]
