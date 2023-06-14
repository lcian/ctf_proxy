FROM python:3.10

COPY proxy /proxy

WORKDIR /proxy

RUN pip install -r requirements.txt

RUN apt update
RUN apt install -y vim nano

CMD ["python3", "proxy.py"]
