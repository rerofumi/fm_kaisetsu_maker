# ローカルの VOICEVOX engine にクエリを投げてテキストを mp3 音声に変換する

import json
import requests
import io
from pydub import AudioSegment


VOICEVOX_HOST = "localhost"
VOICEVOX_PORT = 50021

def generate_speech(text, speaker_id, output_path):
  params={
    "speaker": speaker_id,
    "text": text,
    "speedScale": 0.85,
    "pitchScale": 1.0,
    "intonationScale": 1.0,
    "volumeScale": 1.0,
    "pauseMiddle": 0.0,
    "pauseLong": 0.0,
  }
  # クエリ作成
  query = requests.post(
    f'http://{VOICEVOX_HOST}:{VOICEVOX_PORT}/audio_query',
    params=params
  )
  # クエリ結果から音声生成
  synthesis = requests.post(
      f'http://{VOICEVOX_HOST}:{VOICEVOX_PORT}/synthesis',
      headers = {"Content-Type": "application/json"},
      params = params,
      data = json.dumps(query.json())
  )
  voice = synthesis.content
  # voice を mp3 に変換して保存
  voice_io = io.BytesIO(voice)
  audio = AudioSegment.from_file(voice_io, format="wav", frame_rate=24000, channels=1)
  audio.export(output_path, format="mp3", bitrate="64k")

