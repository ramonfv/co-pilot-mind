import json
from pathlib import Path
from threading import Thread, Event
from audioAquisition.recorder import UserMicRecorder
from audioAquisition.recorder import SystemAudioRecorder
from audioAquisition.recorder import MetadataLogger
import sounddevice as sd
import re

stop_event = Event()


def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\t\n\r]', '_', name)



def load_config():
    base_path = Path(__file__).resolve().parent.parent 
    config_path = base_path / "config" / "record_config.json"

    with open(config_path, "r") as f:
        config = json.load(f)
    config["frame_size"] = int(config["sample_rate"] * config["frame_duration"] / 1000)
    return config


def find_vbcable_device():
    devices = sd.query_devices()
    for index, device in enumerate(devices):
        name = device['name'].lower()
        if "cable output" in name:
            return index, device['name']
    return None, None




def main():


    print("=== CoPilotMind | Captura de Áudio Multi-Canal ===")

    user_id = sanitize_filename(input("User ID: ").strip())
    session_id = sanitize_filename(input("Session ID: ").strip())
    scenario = sanitize_filename(input("Scenario: ").strip())
    cfg = load_config()

    # loopback_device_index, device_name = find_vbcable_device()

    # if loopback_device_index is None:
    #     print("❌ Dispositivo 'CABLE Output' não encontrado. Verifique a instalação do VB-Cable.")
    #     return
    # print(f"✅ Dispositivo VB-Cable detectado: {device_name} (index {loopback_device_index})")




    mic_recorder = UserMicRecorder(user_id, session_id, scenario, cfg)
    # system_recorder = SystemAudioRecorder(user_id, session_id, scenario, cfg, device=loopback_device_index)

    t1 = Thread(target=mic_recorder.record_with_vad, args=(stop_event,))
    # t2 = Thread(target=system_recorder.record_continuous, args=(stop_event,))

    try:
        t1.start()
        # t2.start()

        while t1.is_alive():
            t1.join(timeout=0.1)
            # t2.join(timeout=0.1)

    except KeyboardInterrupt:
        print("\n⏹️ Ctrl+C detectado. Parando gravação...")
        stop_event.set()
        t1.join()
        # t2.join()


    mic_audio_path = mic_recorder.save_audio()
    # sys_audio_path = system_recorder.save_audio()

    MetadataLogger(user_id, session_id, scenario + " (mic)", mic_audio_path).save()
    # MetadataLogger(user_id, session_id, scenario + " (system)", sys_audio_path).save()


if __name__ == "__main__":
    main()