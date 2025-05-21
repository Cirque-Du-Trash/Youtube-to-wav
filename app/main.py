import os
from yt_dlp import YoutubeDL


def download_youtube_audio(url, output_path="downloads/audio"):
    try:
        os.makedirs(output_path, exist_ok=True)

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
            print("오디오 다운로드 시작...")
            info = ydl.extract_info(url, download=True)
            wav_path = os.path.join(output_path, f"{info['title']}.wav")
            print(f"오디오 다운로드 완료: {wav_path}")
            return wav_path

    except Exception as e:
        print(f"오디오 다운로드 중 에러 발생: {str(e)}")
        return None


def download_youtube_video(url, output_path="downloads/video"):
    try:
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
        }

        with YoutubeDL(ydl_opts) as ydl:
            print("비디오 다운로드 시작...")
            info = ydl.extract_info(url, download=True)
            video_path = os.path.join(output_path, f"{info['title']}.mp4")
            print(f"비디오 다운로드 완료: {video_path}")
            return video_path

    except Exception as e:
        print(f"비디오 다운로드 중 에러 발생: {str(e)}")
        return None


if __name__ == "__main__":
    url = input("YouTube URL을 입력하세요: ").strip()
    print("다운로드 유형을 선택하세요:")
    print("1. 오디오 (WAV)")
    print("2. 비디오 (MP4)")
    choice = input("선택 (1 또는 2): ").strip()

    if choice == "1":
        download_youtube_audio(url)
    elif choice == "2":
        download_youtube_video(url)
    else:
        print("잘못된 입력입니다. 1 또는 2를 입력해주세요.")