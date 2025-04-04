from transcriber import Transcriber
from pathlib import Path


def run():

    transcriber = Transcriber(model_size="base")

    transcriber.transcribe(
        wav_path=Path("C:/ReposGithub/co-pilot-mind/data/youtube_wav/103 KM DE JATO_ SOROCABA-GUARULHOS  [EMBRAER PHENOM 300E].wav"),
        scenario="sod_gru",
        user_id="youtube",
        session_id="voo_phemon",
        channel="mixed",  
        language="pt"     
    )


if __name__ == "__main__":
    run()