import os

from pydub import AudioSegment
from yt_dlp import YoutubeDL


def download_youtube_audio(url, output_path="downloads"):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                }
            ],
        }

        with YoutubeDL(ydl_opts) as ydl:
            print("다운로드 시작...")
            info = ydl.extract_info(url, download=True)
            print(f"다운로드 완료: {info['title']}")

            wav_path = os.path.join(output_path, f"{info['title']}.wav")
            print(f"변환 완료: {wav_path}")
            return wav_path

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return None


if __name__ == "__main__":
    url = input("YouTube URL을 입력하세요: ")
    download_youtube_audio(url)
