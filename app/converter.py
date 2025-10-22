import os
import sys
import subprocess


def convert_av1_to_prores(input_path, output_dir=None):
    if not os.path.isfile(input_path):
        print(f"❌ 파일이 존재하지 않습니다: {input_path}")
        return

    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)

    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}_prores.mov")

    print(f"🎬 변환 시작: {input_path}")
    print(f"➡️ 출력: {output_path}")

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "prores_ks",
        "-profile:v", "3",           # ProRes 422 HQ
        "-c:a", "pcm_s16le",         # 무압축 오디오
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 변환 완료: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 변환 중 오류 발생:\n{e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python av1_to_prores.py <input_video_path> [output_dir]")
    else:
        input_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        convert_av1_to_prores(input_path, output_dir)