import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ffmpeg

class VideoHandler(FileSystemEventHandler):
    compatible_codecs = ['h264', 'h265', 'hevc', 'mpeg4', 'vp9']

    def __init__(self, path):
        self.path = path
        self.process_existing_files()

    def process_existing_files(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(('.mp4', '.avi', '.mov')):
                    self.transcode_video(os.path.join(root, file))

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.mp4', '.avi', '.mov')):
            self.transcode_video(event.src_path)

    def transcode_video(self, src_path):
        try:
            # 获取视频编码信息
            probe = ffmpeg.probe(src_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                print(f"No video stream found in {src_path}")
                return

            codec_name = video_stream['codec_name']
            if codec_name not in self.compatible_codecs:
                output_path = os.path.splitext(src_path)[0] + '_transcoded.mp4'
                ffmpeg.input(src_path).output(output_path, vcodec='libx264').run()
                print(f"Transcoded {src_path} to {output_path}")

                # 重命名源文件
                old_path = src_path + '.old_'
                os.rename(src_path, old_path)
                print(f"Renamed original file {src_path} to {old_path}")
            else:
                print(f"{src_path} is already in a compatible format ({codec_name}), no transcoding needed.")
        except ffmpeg.Error as e:
            print(f"Error processing {src_path}: {e}")

if __name__ == "__main__":
    path = "/data/files"  # 替换为你要监控的目录
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()