import subprocess
from pathlib import Path
from datetime import datetime
import json

class KaldiTranscriber:
    def __init__(self, kaldi_script: str = "kaldi_transcriber/pipeline.sh", output_dir="data/transcriptions"):
        self.kaldi_script = Path(kaldi_script).resolve()
        self.output_dir = Path(__file__).resolve().parent.parent / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def transcribe(
        self,
        wav_path: Path,
        scenario: str,
        user_id: str = "default_user",
        session_id: str = "default_session",
        channel: str = "mixed"
    ) -> Path:

        wav_path = wav_path.resolve()
        if not wav_path.exists():
            raise FileNotFoundError(f"❌ Arquivo de áudio não encontrado: {wav_path}")

        output_path = self.output_dir / user_id / session_id
        output_path.mkdir(parents=True, exist_ok=True)

        file_name = f"{scenario}_{channel}_transcription_kaldi.json"
        final_path = output_path / file_name

        print(f"🎧 Transcrevendo com Kaldi: {wav_path.name}...")

        try:
            # Executa o script shell com o caminho para o .wav
            result = subprocess.run([
                "bash", str(self.kaldi_script), str(wav_path)
            ], capture_output=True, text=True, check=True)

            raw_text = result.stdout.strip()
            print("✅ Kaldi retornou resultado com sucesso")

            data = {
                "user_id": user_id,
                "session_id": session_id,
                "scenario": scenario,
                "channel": channel,
                "model": "kaldi",
                "raw_text": raw_text,
                "audio_path": str(wav_path),
                "timestamp": datetime.now().isoformat(),
            }

            with open(final_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"✅ Transcrição Kaldi salva em: {final_path}")
            return final_path

        except subprocess.CalledProcessError as e:
            print("❌ Erro ao executar Kaldi:", e.stderr)
            raise
