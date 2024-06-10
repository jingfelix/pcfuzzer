FROM python:3.10-slim

LABEL maintainer="jingfelix@outlook.com"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ARG TARGET
ARG VERSION

ENV TARGET_VERSION=$TARGET==$VERSION
ENV TARGET=$TARGET

RUN mkdir /result

COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt -i https://mirrors.hust.edu.cn/pypi/web/simple/
RUN pip3 install --no-cache-dir --upgrade $TARGET==$VERSION -i https://mirrors.hust.edu.cn/pypi/web/simple/

CMD python /app/app.py run $TARGET
