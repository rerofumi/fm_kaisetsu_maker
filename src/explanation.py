import time
from .image_compose import ImageComposer
from .movie_clip import MovieClip
from .voicevox_bridge import generate_speech

BG_IMAGE = "background.png"
PERSON_A_IMAGE = "person_a.png"
PERSON_B_IMAGE = "person_b.png"
FONT_FILE = "NotoSansJP-Medium.ttf"
PERSON_A_TALKER = "alloy"
PERSON_B_TALKER = "nova"

MAX_RETRY_COUNTS = 5


class Explanation:
    def __init__(self, api, config_dir, output_dir, use_voicevox=False):
        self.api = api
        self.config_dir = config_dir
        self.output_dir = output_dir
        self.font = self.config_dir + "/font/" + FONT_FILE
        self.use_voicevox = use_voicevox
        self.speaker_id_a = 2
        self.speaker_id_b = 3
        self.access_time = time.time()
        # 掛け合い設定ファイルの読み込み
        with open(self.config_dir + "/talk_system.txt", "r", encoding="utf-8") as f:
            self.explanation_system = f.read()
        # 画像生成設定ファイルの読み込み
        with open(self.config_dir + "/image_background.txt", "r", encoding="utf-8") as f:
            self.image_text_bg = f.read()
        with open(self.config_dir + "/image_person_a.txt", "r", encoding="utf-8") as f:
            self.image_text_a = f.read()
        with open(self.config_dir + "/image_person_b.txt", "r", encoding="utf-8") as f:
            self.image_text_b = f.read()
        # VOICEVOX 用話者 ID 設定ファイルの読み込み
        with open(self.config_dir + "/voicevox_speaker_id.txt", "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                if line.startswith("A:"):
                    self.speaker_id_a = int(line[2:].strip())
                elif line.startswith("B:"):
                    self.speaker_id_b = int(line[2:].strip())
                line = f.readline()


    def generate(self, question, image_only=False, keep_image=False, make_slide_image=False):
        # 画像の生成
        if not keep_image:
            print("generate background image files...")
            self._generate_image(self.image_text_bg, BG_IMAGE)
            print("generate person A image files...")
            self._generate_image(self.image_text_a, PERSON_A_IMAGE)
            print("generate person B image files...")
            self._generate_image(self.image_text_b, PERSON_B_IMAGE)
        # 掛け合いシナリオの生成
        if (image_only and make_slide_image) or (not image_only):
            print("generate talk scenario...")
            talks = self._generate_talks(question)
        # スライド用画像の生成
        if make_slide_image:
            print("generate slide image files...")
            for i, talk in enumerate(talks):
                print(f"({i+1}/{len(talks)})...")
                if talk[0] == "A":
                    self._generate_slide_image(question, talks, i)
        # 解説動画の生成
        if not image_only:
            print("generate speech files...")
            self._generate_speech(talks)            
            print("generate pages...")
            ic = ImageComposer(BG_IMAGE, PERSON_A_IMAGE, PERSON_B_IMAGE, self.font)
            mc = MovieClip()
            for i, talk in enumerate(talks):
                print(f"({i+1}/{len(talks)})...")
                ic.set_slide(f"slide_{i}.png")
                ic.compose(talk).save(f"output/page_{i}.png")
                mc.add(f"output/page_{i}.png", f"output/speech_{i}.mp3")
            print("output movie file...")
            mc.save("output/kaisetsu_movie.mp4")
        #
        print("done.")
    
    # ゆっくり解説風掛け合いの生成
    def _generate_talks(self, question):
        talks = []
        response = self.api.call_llm_chatgpt4turbo(self.api.build_llm_request(self.explanation_system, question))
        body = self.api.extract_text_from_llm_response(response).split("\n")
        for line in body:
            if line.startswith("[A] "):
                talks.append(("A", line[4:]))
            elif line.startswith("[B] "):
                talks.append(("B", line[4:]))
        return talks

    # 音声ファイルの生成
    def _generate_speech(self, talks):
        for i, talk in enumerate(talks):
            print(f"({i+1}/{len(talks)})...")
            if self.use_voicevox:
                # VOICEVOX engine による音声生成
                talker = self.speaker_id_a if talk[0] == "A" else self.speaker_id_b
                generate_speech(talk[1], talker, self.output_dir + f"/speech_{i}.mp3")
            else:
                # OpenAI API による音声生成
                talker = PERSON_A_TALKER if talk[0] == "A" else PERSON_B_TALKER
                response = self.api.generate_speech(talker, talk[1])
                self.api.save_binary(response, self.output_dir + f"/speech_{i}.mp3")

    # 画像の生成
    def _generate_image(self, text, filename, lite=False):
        for i in range(MAX_RETRY_COUNTS):
            try:
                if lite:
                    response = self.api.generate_image_lite(text)
                else:
                    response = self.api.generate_image(text)
                break
            except Exception as e:
                print(str(e) + f" (retrying... {i+1}/{MAX_RETRY_COUNTS})")
                if i < MAX_RETRY_COUNTS - 1:  # i is zero indexed
                    interval = time.time() - self.access_time
                    if interval < 12:
                        time.sleep(12.5 - interval)
                    self.access_time = time.time()
                else:
                    print("Max retries exceeded. Change to safe image.")
                    safe_image = "A peaceful landscape depicting a serene lake surrounded by lush green trees under a clear blue sky. There are colorful flowers blooming along the lakes edge, and a small wooden boat is gently floating on the calm water. In the background, there are rolling hills and a bright sun shining in the sky, casting a warm glow over the entire scene. This image is tranquil and idyllic, showcasing the beauty of nature without any human elements or specific cultural references."
                    response = self.api.generate_image_lite(safe_image)
                    break
        self.api.save_image(self.api.download_image_from_url(
            self.api.extract_image_url_from_dall_e_response(response)), self.output_dir + "/" + filename)
        self.access_time = time.time()

    # スライド用画像の生成
    def _generate_slide_image(self, question, talks, step=0):
        # 1分間に 6 回までしか API を呼べないので、間を空ける
        interval = time.time() - self.access_time
        if interval < 12:
            time.sleep(12.5 - interval)
        self.access_time = time.time()
        # 画像生成
        self._generate_image(talks[step][1], f"slide_{step}.png", False)

