from downloader import YouTubeAudioDownloader

def run():
    yt = YouTubeAudioDownloader("https://www.youtube.com/watch?v=ABhe_bDbplg")
    mp3_path = yt.download_audio()
    wav_path = yt.convert_to_wav(mp3_path)

if __name__ == "__main__":
    run()