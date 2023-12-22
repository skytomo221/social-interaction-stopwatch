
# See https://qiita.com/wakaba130/items/3d215cbf62b7de4100e1

FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

ARG OPENCV_VERSION="4.5.5"
ARG PYTHON_VERSION="3.8"

# like tool
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    vim unzip byobu wget tree git cmake\
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# install python
RUN apt-get update && apt-get install -y python3-dev python3-pip && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN pip3 install -U pip

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# need for opencv
RUN pip3 install -U numpy

# need for opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev libgtk-3-dev \
    libavformat-dev libswscale-dev libhdf5-serial-dev qt5-default \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libopenblas-dev libgflags-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

WORKDIR /tmp

# install opencv
RUN wget -c https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz && \
    tar -zxvf ${OPENCV_VERSION}.tar.gz && rm ${OPENCV_VERSION}.tar.gz && \
    mkdir /tmp/opencv-${OPENCV_VERSION}/build && \
    wget -c https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.tar.gz && \
    tar -zxvf ${OPENCV_VERSION}.tar.gz && rm /tmp/${OPENCV_VERSION}.tar.gz && \
    cd /tmp/opencv-${OPENCV_VERSION}/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages \
        -D WITH_TBB=ON \
        -D ENABLE_FAST_MATH=1 \
        -D CUDA_FAST_MATH=1 \
        -D WITH_CUBLAS=1 \
        -D WITH_CUDA=ON \
        -D WITH_CUDNN=ON \
        -D BUILD_opencv_cudacodec=OFF \
        -D OPENCV_DNN_CUDA=ON \
        -D CUDA_ARCH_BIN="7.5, 8.0" \
        -D WITH_V4L=ON \
        -D WITH_QT=ON \
        -D WITH_OPENGL=ON \
        -D WITH_GSTREAMER=ON \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-${OPENCV_VERSION}/modules \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D INSTALL_C_EXAMPLES=OFF \
        -D BUILD_opencv_python2=OFF \
        -D BUILD_opencv_python3=ON \
        -D BUILD_EXAMPLES=OFF .. && \
    make -j20 && make install && ldconfig && \
    rm -rf /tmp/opencv-${OPENCV_VERSION} /tmp/opencv_contrib-${OPENCV_VERSION}

WORKDIR /
