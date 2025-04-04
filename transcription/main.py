from whisper_transcriber.transcriber import WhisperTranscriber
from pathlib import Path

def run():
    transcriber = WhisperTranscriber(model_size="turbo")

    transcriber.transcribe(
        wav_path=Path(__file__).resolve().parent.parent / "data/youtube_wav/103 KM DE JATO_ SOROCABA-GUARULHOS  [EMBRAER PHENOM 300E].wav",
        scenario="sod_gru",
        user_id="youtube",
        session_id="voo_phenom",
        channel="mixed"
    )

if __name__ == "__main__":
    run()
