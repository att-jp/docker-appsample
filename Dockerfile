FROM alpine:3.6
MAINTAINER shkawan@microsoft.com

RUN apk update && apk add python2 py-pip git openrc mongodb tzdata curl
RUN mkdir -p /data/db

COPY *.py ./
COPY entry.sh ./
COPY requirements.txt ./
COPY VERSION ./

RUN pip install -r requirements.txt

USER nobody

ENV TZ Asia/Tokyo

CMD [ "./entry.sh" ]
