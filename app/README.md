# YouTube to WAV Converter

YouTube 동영상의 URL을 입력하면 WAV 오디오 파일로 변환하여 다운로드하는 프로그램입니다.

## 사전 요구사항

### Windows 사용자

1. [ffmpeg 다운로드](https://www.gyan.dev/ffmpeg/builds/)
   - ffmpeg-release-essentials.zip 파일을 다운로드
   - 압축 해제 후 bin 폴더의 경로를 시스템 환경 변수 PATH에 추가

### macOS 사용자

1. Homebrew 설치 (없는 경우)
``` bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. ffmpeg 설치
``` bash
brew install ffmpeg
```


## 설치 방법

### 소스 코드로 실행

1. Python 3.12 이상 설치

2. Poetry 설치
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. 프로젝트 클론
```bash
git clone https://github.com/yourusername/youtube-to-wav.git
cd youtube-to-wav
cd app
```

4. 의존성 설치
```bash
poetry install
```

5. 프로그램 실행
```bash
poetry run python main.py
```

## 사용 방법

1. 프로그램 실행
2. YouTube 동영상 URL 입력
3. 변환된 WAV 파일은 `downloads` 폴더에 저장됨

## 주의사항

- 저작권이 있는 콘텐츠의 다운로드는 법적 문제가 될 수 있습니다
- 안정적인 인터넷 연결이 필요합니다
- 파일 크기에 따라 변환 시간이 달라질 수 있습니다

## 문제 해결

### ffmpeg 관련 오류
- ffmpeg가 올바르게 설치되어 있는지 확인
- 시스템 환경 변수 PATH에 ffmpeg가 추가되어 있는지 확인

### 다운로드 실패
- 인터넷 연결 상태 확인
- YouTube URL이 올바른지 확인
- 비공개 또는 연령 제한이 있는 동영상은 다운로드가 제한될 수 있음

## 라이선스

MIT License

## 기여하기

버그 리포트나 기능 제안은 GitHub Issues를 통해 제출해 주세요.