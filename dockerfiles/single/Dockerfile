#
# restock:latest
#
# Build docker image:
# docker build -t restock -f dockerfiles/single/Dockerfile .
#
# Run container:
# docker run -it --name restock restock /bin/bash
# docker run --entrypoint /bin/bash -i -t restock
#
# Reference:
# https://docs.docker.com/get-started/
# https://hub.docker.com/help/

FROM python:3

WORKDIR /ReStock
COPY . /ReStock
RUN pip install -r requirements.txt
RUN pip install -e .
EXPOSE 5000
ENTRYPOINT ["python", "restock/app.py"]
