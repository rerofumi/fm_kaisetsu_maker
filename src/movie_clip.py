from moviepy.editor import ImageClip, AudioFileClip, AudioClip, concatenate_videoclips

class MovieClip:
  def __init__(self):
    self.clips = []

  def add(self, image_file, speech_file):
    audio = AudioFileClip(speech_file)
    image = ImageClip(image_file, duration=audio.duration+1.5)
    # 後ろの0.15秒を切り捨ててるのは AudioFileClip でノイズが入るため、その対処療法
    clip = image.set_audio(audio.subclip(0, -0.15))
    self.clips.append(clip)
  
  def save(self, output_file):
    final_clip = concatenate_videoclips(self.clips)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=30)
