FROM ubuntu:18.04

LABEL maintainer="Fernando Furusato <ferseiti@gmail.com>"

USER root

RUN apt-get update && apt-get install -y python3-pip
    
RUN /usr/bin/pip3 install -v matplotlib \
    jupyter \
    scikit-image \
    numpy \
    tensorflow \
    keras \
    h5py \
    requests \
    opencv-python \
    scipy==1.1.0

RUN apt-get update && apt-get install -y libgtk2.0-dev

RUN mkdir /root/uploaded_data/

COPY data.tar.gz /root/uploaded_data/

RUN tar /root/uploaded_data/data.tar.gz --directory /root/uploaded_data/

EXPOSE 8888
WORKDIR /root/

ENV DOCKER 1

CMD jupyter notebook --no-browser --allow-root --ip=0.0.0.0
