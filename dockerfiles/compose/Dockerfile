#
# restocked:latest
#
# to build docker image:
# docker build -t restocked -f dockerfiles/Dockerfile .
#
# to run:
# docker run -it --name restocked /bin/bash
#

FROM centos:7

MAINTAINER Kai Munechika "kaim@bu.edu"
COPY . /ReStock
COPY requirements.txt /tmp
WORKDIR /tmp
RUN yum install -y python-devel && yum clean all
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py && rm get-pip.py
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "src/web/app.py"]
