import whisper
from pathlib import Path
from datetime import datetime
import json
import time
from slugify import slugify


class WhisperTranscriber:
    def __init__(self, model_size, output_dir="data/transcriptions/youtube/voo_phemon"):
        self.model = whisper.load_model(model_size)
        self.model_size = model_size
        self.output_dir = Path(__file__).resolve().parent.parent / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def transcribe(
        self,
        wav_path: Path,
        scenario: str,
        user_id: str = "default_user",
        session_id: str = "default_session",
        channel: str = "mixed",
        language: str = None
    ) -> Path:

        wav_path = wav_path.resolve()

        if not wav_path.exists():
            raise FileNotFoundError(f"❌ Arquivo de áudio não encontrado: {wav_path}")

        print(f"🎧 Transcrevendo: {wav_path.name} usando Whisper-{self.model_size}...")

        start_time = time.time()
        result = self.model.transcribe(str(wav_path), language=language)
        duration = time.time() - start_time
        print(f"🕒 Transcrição concluída em {duration:.2f} segundos")

        data = {
            "user_id": user_id,
            "session_id": session_id,
            "scenario": scenario,
            "channel": channel,
            "model": self.model_size,
            "language": result.get("language", language),
            "raw_text": result["text"],
            "segments": result.get("segments", []),
            "audio_path": str(wav_path),
            "timestamp": datetime.now().isoformat(),
            "processing_time_seconds": round(duration, 2)
        }

        output_path = self.output_dir / user_id / session_id
        output_path.mkdir(parents=True, exist_ok=True)

        file_name = f"{slugify(scenario)}_{channel}_transcription.json"
        final_path = output_path / file_name

        with open(final_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"✅ Transcrição salva em: {final_path}")
        return final_path
