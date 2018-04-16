#
# restocked:latest
#
# to build docker image:
# docker build -t restocked -f dockerfiles/single/Dockerfile .
#
# to run:
# docker run -it --name restocked restocked /bin/bash
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
CMD export PYTHONPATH=/ReStock
ENTRYPOINT ["python", "/ReStock/src/web/app.py"]

#TODO: Fix me!

(venv) [ecerquei@dev ReStock]$ docker start -i restocked
Traceback (most recent call last):
  File "/ReStock/src/web/app.py", line 7, in <module>
    from src.db.mongo_util import *
ImportError: No module named src.db.mongo_util

