import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

class ImageComposer:
  def __init__(self, bg_file, p_a_file, p_b_file, font):
    self.bg_file = Image.open("output/"+bg_file).convert('RGBA')
    self.p_a_file = Image.open("output/"+p_a_file).convert('RGBA')
    self.p_b_file = Image.open("output/"+p_b_file).convert('RGBA')
    self.font = ImageFont.truetype(font, 42)
    self.slide = None
  
  def set_slide(self, slide):
    # slide で示された画像ファイルが存在するか確認
    # あれば slide をセット
    if os.path.isfile("output/"+slide):
      self.slide = Image.open("output/"+slide).convert('RGBA')

  def compose(self, talk):
    if talk[0] == "A":
      return self._compose_image(talk[1], "A")
    else:
      return self._compose_image(talk[1], "B")
  
  def _compose_image(self, text, name="A"):
    screen = Image.new("RGBA", (1920, 1080), (255, 255, 255))
    screen.paste(self.bg_file.resize((1920,1920)), (0, -420))
    box = Image.new("RGBA", screen.size)
    draw = ImageDraw.Draw(box, "RGBA")
    # slide
    if self.slide is not None:
      screen.paste(self.slide.resize((800,800)), (560, 20))  
    # textbox
    draw.rectangle([(20, 700), (1900, 1040)], fill=(0, 0, 0, 180))
    # text
    wrapped_text = textwrap.fill(text, width=28)
    draw.text((340, 740), wrapped_text, fill=(255, 255, 255, 255), font=self.font)
    # alpha render
    screen = Image.alpha_composite(screen, box)
    # person
    ay = by = 750
    if name == "A":
      ay = 720
    else:
      by = 720
    screen.paste(self.p_a_file.resize((250,250)), (40, ay))
    screen.paste(self.p_b_file.resize((250,250)), (1630, by))
    return screen
