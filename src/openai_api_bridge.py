from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# OpenAI API Bridge
# OpenAP API を呼び出すためのブリッジクラス、コンストラクタでAPIキーを設定する
class OpenAIAPIBridge:
  
  def __init__(self, api_key):
    self.client = OpenAI(api_key = api_key)

  # ChatGPT を使用する LLM 呼び出しメソッド
  # prompt: プロンプト文字列
  # engine: 使用するエンジン
  def call_llm(self, prompts, engine):
    response = self.client.chat.completions.create(
      model=engine,
      messages=prompts,
      temperature=0.2,
      max_tokens=4000,
    )
    return response
  
  # ChatGPT-4-turbo エンジンに限定した LLM 呼び出しメソッド
  # prompt: プロンプト文字列
  def call_llm_chatgpt4turbo(self, prompts):
    return self.call_llm(prompts, "gpt-4-1106-preview") 

  # ChatGPT-3-turbo エンジンに限定した LLM 呼び出しメソッド
  # prompt: プロンプト文字列
  def call_llm_chatgpt3turbo(self, prompts):
    return self.call_llm(prompts, "gpt-3.5-turbo") 

  # Dall-E での画像生成メソッド
  def generate_image(self, prompts):
    response = self.client.images.generate(
      model="dall-e-3",
      prompt=prompts,
      size="1024x1024",
      quality="standard",
      n=1,
    )
    return response

  # TTS での音声生成メソッド
  def generate_speech(self, talker, prompts):
    response = self.client.audio.speech.create(
      input=prompts,
      model="tts-1",
      voice=talker, # "alloy", "echo", "fable", "onyx", "nova", "shimmer"
      response_format="mp3",
      speed=1.2,
    )
    return response

  # LLM リクエスト構築
  def build_llm_request(self, system, user):
    return [
      { "role": "system", "content": system },
      { "role": "user", "content": user},
    ]
  
  # LLM のレスポンスからテキストだけを抽出する
  def extract_text_from_llm_response(self, response):
    return response.choices[0].message.content
  
  # 生成された画像の URL を抽出する
  def extract_image_url_from_dall_e_response(self, response):
    return response.data[0].url  

  # 生成された画像に URL でアクセスしてダウンロードし PIL イメージオブジェクトにして返す
  def download_image_from_url(self, url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

  # 生成された画像をファイルに保存する
  def save_image(self, image, path):
    image.save(path)

  # 生成されたバイナリをファイルに保存する
  def save_binary(self, binary, path):
    with open(path, 'wb') as f:
      f.write(binary.content)
