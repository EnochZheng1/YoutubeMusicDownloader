from pytube import YouTube
import os

video = YouTube(str(input("Youtube URL: \n>")))
audio = video.streams.filter(only_audio = True).first()
destination = str(input("Enter Download Path: \n>")) or "."
output = audio.download(output_path=destination)
base, ext = os.path.splitext(output)
file = base + ".mp3"
os.rename(output, file)
print(video.title + "'s audio is downloaded to " + destination)