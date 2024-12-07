import subprocess
import os
def preprocess_video(file_path, output_path, resolution="1280x720", fps=30):
    try:
        # 检查输出文件路径所在的目录是否存在
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # 如果目录不存在，创建目录

        # 设置FFmpeg路径
        ffmpeg_path = r"F:\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
        # 构造FFmpeg命令
        command = [
            ffmpeg_path, "-i", file_path,  # 输入文件
            "-c:v", "libx264",  # 使用H.264编码（广泛兼容）
            "-preset", "fast",  # 使用快速编码预设
            "-c:a", "aac",  # 音频编码为AAC
            "-b:a", "128k",  # 音频比特率为128k
            "-movflags", "+faststart",  # 提前写入元数据，适配流式播放
            "-s", resolution,  # 设置分辨率
            "-r", str(fps),  # 设置帧率
            output_path  # 输出文件路径（包括文件名）
        ]
        # 输出调试信息
        print(f"正在修复视频: {file_path}")
        print("执行的命令:", " ".join(command))
        # 执行FFmpeg命令
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 根据返回结果检查处理是否成功
        if result.returncode == 0:
            print(f"视频修复成功，保存到: {output_path}")
            return True
        else:
            print("视频修复失败，错误信息如下:")
            print(result.stderr.decode())
            return False

    except Exception as e:
        print("修复过程中出现错误:", str(e))
        return False

file_path = 'F:\\yolov5\\yolov5\\web\\web\\static\\result\\12月4日.mp4'
output_path = 'F:\\yolov5\\yolov5\\web\\web\\static\\result\\output_video.mp4'
preprocess_video(file_path, output_path)
