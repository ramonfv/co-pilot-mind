from transcriber import Transcriber
from pathlib import Path


def run():

    transcriber = Transcriber(model_size="base")

    transcriber.transcribe(
        wav_path=Path("C:/ReposGithub/co-pilot-mind/capture/audio_data/Ramon/paperAcquisition/mic/paperAcquisition_mic.wav"),
        scenario="paperAcquisition",
        user_id="ramon",
        session_id="1",
        channel="mixed",  
        language="pt"     
    )


if __name__ == "__main__":
    run()