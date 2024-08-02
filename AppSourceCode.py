from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from pytube import YouTube
import os

class DownloaderApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.url_input = TextInput(hint_text="Enter YouTube URL")
        self.main_layout.add_widget(self.url_input)
        
        self.audio_video_spinner = Spinner(text="Audio", values=("Audio", "Video"))
        self.main_layout.add_widget(self.audio_video_spinner)

        self.quality_spinner = Spinner(text="High", values=("High", "Low"))
        self.main_layout.add_widget(self.quality_spinner)

        self.download_button = Button(text="Download")
        self.download_button.bind(on_press=self.download_media)
        self.main_layout.add_widget(self.download_button)

        return self.main_layout

    def download_media(self, instance):
        video_url = self.url_input.text

        if not video_url.strip():
            print("Please enter a valid YouTube URL.")  # Adapt this to show an error in the UI
            return

        try:
            video = YouTube(video_url)
        except:
            print("An error occurred.")
            return

        destination = "."  # Change this to where you want to save the file

        try:
            if self.audio_video_spinner.text == 'Audio':
                audio = video.streams.get_audio_only()
                output = audio.download(output_path=destination)
                base, ext = os.path.splitext(output)
                file = base + ".mp3"
                os.rename(output, file)
            elif self.audio_video_spinner.text == 'Video':
                if self.quality_spinner.text == 'High':
                    video_stream = video.streams.get_highest_resolution()
                elif self.quality_spinner.text == 'Low':
                    video_stream = video.streams.get_lowest_resolution()
                video_stream.download(output_path=destination)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return

        print(f"{video.title}'s {self.audio_video_spinner.text} is downloaded to {destination}")

if __name__ == "__main__":
    DownloaderApp().run()
