import os
import shutil
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


def _get_common_opts(use_cookies=True):
    """공통 yt-dlp 옵션"""
    opts = {
        "outtmpl_na_placeholder": "NA",
        "noplaylist": True,
        "restrictfilenames": True,
        "continuedl": False,  # 이전 세션의 만료된 URL로 resume 시도 방지
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 30,
        "concurrent_fragment_downloads": 1,
        "progress_hooks": [_progress_hook],
        "quiet": False,
        "verbose": True,
        "source_address": "0.0.0.0",
        "extractor_args": {
            "youtube": {
                # android_sdkless는 YouTube에 의해 차단됨 — 제외
                "player_client": ["default", "-android_sdkless"],
            }
        },
        # EJS 챌린지 스크립트를 GitHub에서 자동 다운로드
        "remote_components": {"ejs:github"},
    }

    # JS 런타임 자동 감지 (Deno만 기본 활성화, Node/Bun은 명시적 설정 필요)
    js_runtimes = {}
    for runtime in ("node", "bun", "deno"):
        rt_path = shutil.which(runtime)
        if rt_path:
            js_runtimes[runtime] = {"path": rt_path}
    if js_runtimes:
        opts["js_runtimes"] = js_runtimes

    # 브라우저 쿠키를 사용하여 HD 포맷 접근 (SABR/403 우회)
    if use_cookies:
        opts["cookiesfrombrowser"] = ("chrome",)

    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        opts["ffmpeg_location"] = os.path.dirname(ffmpeg_path)

    return opts


def _run_download(ydl_opts, url):
    """쿠키 로드 실패 시 쿠키 없이 재시도"""
    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
    except Exception as e:
        if "cookiesfrombrowser" in ydl_opts and "cookie" in str(e).lower():
            print("⚠️  브라우저 쿠키 로드 실패 — 쿠키 없이 재시도합니다...")
            ydl_opts_no_cookies = {k: v for k, v in ydl_opts.items() if k != "cookiesfrombrowser"}
            with YoutubeDL(ydl_opts_no_cookies) as ydl:
                return ydl.extract_info(url, download=True)
        raise


def download_youtube_audio(url, output_path="downloads/audio"):
    try:
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            **_get_common_opts(),
            "format": "140/bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                }
            ],
        }

        print("오디오 다운로드 시작...")
        info = _run_download(ydl_opts, url)
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
            **_get_common_opts(),
            "format": "bestvideo+bestaudio/best",
            "format_sort": ["res", "vcodec:vp9.2", "acodec:opus"],
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "postprocessor_args": {
                # Apple Silicon Mac용 하드웨어 인코더
                "merger": [
                    "-c:v", "h264_videotoolbox", "-b:v", "8M",
                    "-c:a", "aac", "-b:a", "192k",
                ],
            },
        }

        print("비디오 다운로드 시작...")
        info = _run_download(ydl_opts, url)
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