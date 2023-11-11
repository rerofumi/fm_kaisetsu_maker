from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

class MovieClip:
  def __init__(self):
    self.clips = []

  def add(self, image_file, speech_file):
    audio = AudioFileClip(speech_file)
    image = ImageClip(image_file, duration=audio.duration+1.5)
    clip = image.set_audio(audio)
    self.clips.append(clip)
  
  def save(self, output_file):
    final_clip = concatenate_videoclips(self.clips)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=30)
