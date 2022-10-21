# Microservice skeleton
# VERSION 1.0.0
# MAINTAINER lifangjun <lifj@ebondhm.com>
FROM python:3.9.9

ENV LANG=C.UTF-8
RUN apt-get update \
&&  apt-get  upgrade -y \
&&  apt-get install -y curl \
&&  apt-get install poppler-utils libgl1-mesa-glx -y \
&&  apt-get install -y inetutils-ping \
&&  apt-get install -y vim \
&&  apt-get install  openssh-server  openssh-client  -y \
&&  echo "Asia/Shanghai" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r /tmp/requirements.txt
WORKDIR /usr/src/backend
COPY . .
RUN chmod +x ./deploy/start_server.sh