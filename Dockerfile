FROM standardcore/python-ffmpeg:slim-240730-ca65

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . /app

# 安装所需的 Python 包
RUN pip install --no-cache-dir watchdog ffmpeg-python

# 安装 ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV PATH="/app:${PATH}"

# 运行主程序
CMD ["python", "main.py"]