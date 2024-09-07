FROM python:3-alpine

ENV port 8343
ENV path "?"
ENV addresses "?"

RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

CMD python /etc/app/enocean_webthing.py $port $path $addresses



