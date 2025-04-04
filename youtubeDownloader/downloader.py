import subprocess
from pathlib import Path
import re

class YouTubeAudioDownloader:
    def __init__(self, url: str, output_dir: str = "data/youtube_wav"):
        self.url = url
        self.output_dir = Path(__file__).resolve().parent.parent  / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    
    def get_video_title(self):
        cmd = ["yt-dlp", "--get-title", self.url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()
    
    def sanitize_filename(self, name: str):
        return re.sub(r'[<>:"/\\|?*\n\r\t]', "_", name)

    def download_audio(self) -> Path:
        filename = self.get_video_title()
        filename = self.sanitize_filename(filename) + ".webm"
        output_path = self.output_dir / filename

        if output_path.exists():
            print(f"✅ Arquivo já existe: {filename}")
            return output_path

        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-o", str(output_path),
            self.url
        ]
        subprocess.run(cmd, check=True)
        return output_path

    def convert_to_wav(self, input_path: Path, output_name=None) -> Path:
        output_name = self.get_video_title() + ".wav" if output_name is None else output_name
        output_name = self.sanitize_filename(output_name)
        output_path = input_path.parent / output_name
        cmd = f'ffmpeg -y -i "{input_path}" -ar 16000 -ac 1 "{output_path}"'
        subprocess.run(cmd, shell=True)
        return output_path