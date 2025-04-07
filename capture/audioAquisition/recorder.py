import datetime
import os
import json
import queue
import webrtcvad
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime



class MetadataLogger:
    def __init__(self, user_id, session_id, scenario, audio_path):
        self.user_id = user_id
        self.session_id = session_id
        self.scenario = scenario
        self.audio_path = audio_path
        self.timestamp = datetime.now().isoformat()
        self.folder = f"audio_data/{self.user_id}/{self.session_id}/{self.scenario}/mic"
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
    

class UserMicRecorder:
    def __init__(self, user_id, session_id, scenario, config, device=None):
        self.user_id = user_id
        self.session_id = session_id
        self.scenario = scenario
        self.config = config
        self.device = device
        self.vad = webrtcvad.Vad(config["vad_mode"])
        self.q_audio = queue.Queue()
        self.recorded_frames = []
        self.folder = f"audio_data/{self.user_id}/{self.session_id}/mic"
        os.makedirs(self.folder, exist_ok=True)
        self.output_wav = os.path.join(self.folder, f"{self.session_id}_mic.wav")

    def _callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.q_audio.put(indata.copy())

    def record_with_vad(self, stop_event):
        print("🎤 Gravando microfone com VAD (Operador). Ctrl+C para parar.")
        silence_counter = 0
        speech_buffer = []
        while not stop_event.is_set():
            try:
                with sd.InputStream(samplerate=self.config["sample_rate"],
                                    channels=self.config["channels"],
                                    dtype='int16',
                                    blocksize=self.config["frame_size"],
                                    callback=self._callback,
                                    device=self.device):
                    while True:
                        try:
                            frame = self.q_audio.get(timeout=0.5)
                        except queue.Empty:
                            if stop_event.is_set():
                                break
                            continue
                        frame_bytes = frame.tobytes()
                        is_speech = self.vad.is_speech(frame_bytes, self.config["sample_rate"])

                        if is_speech:
                            speech_buffer.append(frame)
                            silence_counter = 0
                        elif speech_buffer:
                            silence_counter += 1
                            if silence_counter > self.config["max_silence_frames"]:
                                self.recorded_frames.extend(speech_buffer)
                                speech_buffer.clear()
                                silence_counter = 0

            except KeyboardInterrupt:
                print("⏹️ Gravação encerrada pelo usuário.")
                self.recorded_frames.extend(speech_buffer)

    def save_audio(self):
        if self.recorded_frames:
            print(f"🔁 Total de frames gravados (mic): {len(self.recorded_frames)}")
            audio_np = np.concatenate(self.recorded_frames)
            sf.write(self.output_wav, audio_np, self.config["sample_rate"])
            print(f"✅ Áudio do operador salvo em: {self.output_wav}")
            return self.output_wav
        else:
            print("⚠️ Nenhum áudio foi detectado.")
            return None
        

class SystemAudioRecorder:
    def __init__(self, user_id, session_id, scenario, config, device, channel_name):
        self.user_id = user_id
        self.session_id = session_id
        self.scenario = scenario
        self.config = config
        self.device = device  # deve ser o índice do dispositivo loopback
        self.channel_name = channel_name
        self.q_audio = queue.Queue()
        self.frames = []
        self.folder = f"audio_data/{user_id}/{session_id}/{scenario}/{channel_name}"
        os.makedirs(self.folder, exist_ok=True)
        self.output_wav = os.path.join(self.folder, f"{session_id}_{channel_name}.wav")

    def _callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.q_audio.put(indata.copy())

    def record_continuous(self, stop_event):
        print("🎧 Gravando a partir do CABLE Output (VB-Cable). Ctrl+C para parar.")
        while not stop_event.is_set():
            try:
                with sd.InputStream(samplerate=self.config["sample_rate"],
                                    channels=self.config["channels"],
                                    dtype='int16',
                                    blocksize=self.config["frame_size"],
                                    callback=self._callback,
                                    device=self.device):
                    while True:
                        try:
                            frame = self.q_audio.get(timeout=0.5)
                        except queue.Empty:
                            if stop_event.is_set():
                                break
                            continue
                        self.frames.append(frame)
            except KeyboardInterrupt:
                print("⏹️ Gravação encerrada.")




    def save_audio(self):
        if self.frames:
            print(f"🔁 Total de frames capturados (sistema): {len(self.frames)}")
            audio_np = np.concatenate(self.frames)
            sf.write(self.output_wav, audio_np, self.config["sample_rate"])
            print(f"✅ Áudio do sistema salvo em: {self.output_wav}")
            return self.output_wav
        else:
            print("⚠️ Nenhum áudio foi capturado.")
            return None
    