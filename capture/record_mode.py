import datetime
import os
import json
import queue
import webrtcvad
import sounddevice as sd
import soundfile as sf
import numpy as np



class MetadataLogger:
    def __init__(self, user_id, session_id, scenario, audio_path):
        self.user_id = user_id
        self.session_id = session_id
        self.scenario = scenario
        self.audio_path = audio_path
        self.timestamp = datetime.now().isoformat()
        self.folder = f"audio_data/{self.user_id}/{self.session_id}"
        os.makedirs(self.folder, exist_ok=True)
        self.metadata_path = os.path.join(self.folder, f"{self.session_id}_metadata.json")

    def save(self):
        metadata = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "scenario": self.scenario,
            "audio_path": self.audio_path,
            "timestamp": self.timestamp
        }

        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

        print(f"Metadata saved to {self.metadata_path}")
    

class AudioRecorder:
    def __init__(self, user_id, session_id, scenario):
        self.user_id = user_id
        self.session_id = session_id
        self.scenario = scenario
        self.folder = f"audio_data/{self.user_id}/{self.session_id}"
        os.makedirs(self.folder, exist_ok=True)
        self.output_wav = os.path.join(self.folder, f"{self.session_id}_recording.wav")
        self.q_audio = queue.Queue()
        self.vad = webrtcvad.Vad(cfg["vad_mode"])
        self.recorded_frames = []

    def _callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.q_audio.put(indata.copy())

    def record_with_vad(self):
        print("\n🎙️ Gravando com VAD... Pressione Ctrl+C para encerrar.\n")
        silence_counter = 0
        speech_buffer = []

        try:
            with sd.InputStream(samplerate=cfg["sample_rate"], channels= cfg["channels"], dtype='int16',
                                blocksize=cfg["frame_size"], callback=self._callback):
                while True:
                    frame = self.q_audio.get()
                    frame_bytes = frame.tobytes()

                    is_speech = self.vad.is_speech(frame_bytes, cfg["sample_rate"])

                    if is_speech:
                        speech_buffer.append(frame)
                        silence_counter = 0
                    elif speech_buffer:
                        silence_counter += 1
                        if silence_counter > cfg["max_silence_frames"]:
                            self.recorded_frames.extend(speech_buffer)
                            speech_buffer.clear()
                            silence_counter = 0

        except KeyboardInterrupt:
            print("\n⏹️ Gravação finalizada.")
            self.recorded_frames.extend(speech_buffer)

    def save_audio(self):
        if self.recorded_frames:
            audio_np = np.concatenate(self.recorded_frames)
            sf.write(self.output_wav, audio_np, cfg["sample_rate"])
            print(f"✅ Áudio salvo em: {self.output_wav}")
            return self.output_wav
        else:
            print("⚠️ Nenhum áudio detectado.")
            return None
    
def main():
    print("=== CoPilotMind | Captura de Áudio com VAD ===")
    user_id = input("User ID: ")
    session_id = input("Session ID: ")
    scenario = input("Scenario: ")

    recorder = AudioRecorder(user_id, session_id, scenario)
    recorder.record_with_vad()
    audio_path = recorder.save_audio()

    logger = MetadataLogger(user_id, session_id, scenario, audio_path)
    logger.save()



def load_config(path="C:\\ReposGithub\\co-pilot-mind\\config\\record_config.json"):
    with open(path, "r") as f:
        config = json.load(f)
    config["frame_size"] = int(config["sample_rate"] * config["frame_duration"] / 1000)
    return config



if __name__ == "__main__":
    cfg = load_config()
    main()
