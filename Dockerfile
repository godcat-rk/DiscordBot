FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install discord
RUN pip install openai
RUN pip install pytube
RUN pip install yt_dlp
RUN pip install ffmpeg
RUN pip install pip install PyNaCl
RUN apt-get update && apt-get install -y ffmpeg

RUN python -m pip install jupyterlab