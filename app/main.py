import os
import traceback
from yt_dlp import YoutubeDL


def _progress_hook(status_dict):
    status = status_dict.get("status")
    if status == "downloading":
        percent = (status_dict.get("_percent_str") or "").strip()
        speed = (status_dict.get("_speed_str") or "").strip()
        eta = (status_dict.get("_eta_str") or "").strip()
        print(f"진행률 {percent} | 속도 {speed} | ETA {eta}")
    elif status == "finished":
        print("다운로드 완료, 후처리(변환/병합) 진행 중...")

def download_youtube_audio(url, output_path="downloads/audio"):
    try:
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            "format": "140/bestaudio[ext=m4a][protocol!=m3u8]/bestaudio[protocol!=m3u8]/bestaudio/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "outtmpl_na_placeholder": "NA",
            "noplaylist": True,
            "restrictfilenames": True,
            "continuedl": True,
            "retries": 10,
            "fragment_retries": 10,
            "socket_timeout": 30,
            "concurrent_fragment_downloads": 1,
            "progress_hooks": [_progress_hook],
            "ffmpeg_location": "/opt/homebrew/bin",
            "quiet": False,
            "verbose": True,
            "hls_prefer_native": False,
            "external_downloader": "ffmpeg",
            "source_address": "0.0.0.0",
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"],
                }
            },
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
        traceback.print_exc()
        return None


def download_youtube_video(url, output_path="downloads/video"):
    try:
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            "format": "bestvideo[protocol!=m3u8]+bestaudio[protocol!=m3u8]/best[protocol!=m3u8]/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "outtmpl_na_placeholder": "NA",
            "noplaylist": True,
            "restrictfilenames": True,
            "continuedl": True,
            "retries": 10,
            "fragment_retries": 10,
            "socket_timeout": 30,
            "concurrent_fragment_downloads": 1,
            "progress_hooks": [_progress_hook],
            "ffmpeg_location": "/opt/homebrew/bin",
            "quiet": False,
            "verbose": True,
            "hls_prefer_native": False,
            "external_downloader": "ffmpeg",
            "source_address": "0.0.0.0",
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"],
                }
            },
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
        traceback.print_exc()
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