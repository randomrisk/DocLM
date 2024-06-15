FROM python:3.11.2-slim-buster
ENV TZ=Asia/Shanghai
ENV LANG=en_US.UTF-8

RUN apt-get update \
    && apt-get install -y curl vim tzdata \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Asia/Shanghai > /etc/timezone \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /root/.cache \
    && rm -rf /tmp/*

RUN pip install --upgrade pip \
	&& pip install tornado==6.1 --no-cache-dir \
	&& pip install openai[datalib]==0.27.2 --no-cache-dir

WORKDIR /work

COPY src src

CMD python3 src/main.py
