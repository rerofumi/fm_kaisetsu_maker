from .image_compose import ImageComposer
from .movie_clip import MovieClip
from .voicevox_bridge import generate_speech

BG_IMAGE = "background.png"
PERSON_A_IMAGE = "person_a.png"
PERSON_B_IMAGE = "person_b.png"
FONT_FILE = "NotoSansJP-Medium.ttf"
PERSON_A_TALKER = "alloy"
PERSON_B_TALKER = "nova"

class Explanation:
    def __init__(self, api, config_dir, output_dir, use_voicevox=False):
        self.api = api
        self.config_dir = config_dir
        self.output_dir = output_dir
        self.font = self.config_dir + "/font/" + FONT_FILE
        self.use_voicevox = use_voicevox
        self.speaker_id_a = 2
        self.speaker_id_b = 3
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


    def generate(self, question, image_only=False, keep_image=False):
        # 画像の生成
        if not keep_image:
            print("generate background image files...")
            self._generate_image(self.image_text_bg, BG_IMAGE)
            print("generate person A image files...")
            self._generate_image(self.image_text_a, PERSON_A_IMAGE)
            print("generate person B image files...")
            self._generate_image(self.image_text_b, PERSON_B_IMAGE)
        # 解説動画の生成
        if not image_only:
            print("generate talk scenario...")
            talks = self._generate_talks(question)
            print("generate speech files...")
            self._generate_speech(talks)
            #
            print("generate pages...")
            ic = ImageComposer(BG_IMAGE, PERSON_A_IMAGE, PERSON_B_IMAGE, self.font)
            mc = MovieClip()
            for i, talk in enumerate(talks):
                print(f"({i+1}/{len(talks)})...")
                image = ic.compose(talk).save(f"output/page_{i}.png")
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
    def _generate_image(self, text, filename):
        response = self.api.generate_image(text)
        self.api.save_image(self.api.download_image_from_url(self.api.extract_image_url_from_dall_e_response(response)), self.output_dir + "/" + filename)
