FROM standardcore/python-ffmpeg:slim-240730-ca65

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . /app

# 设置环境变量
ENV PATH="/app:${PATH}"

RUN pip install watchdog ffmpeg-python

# 运行主程序
CMD ["python", "main.py"]