from pytube import YouTube
from pytube.exceptions import PytubeError
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os;

def progress_function(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = (size-bytes_remaining)/size
    download_bar['value'] = progress*100
    root.update_idletasks()

def download_media():
    video_url = url_entry.get()

    if not video_url.strip():
        messagebox.showinfo("Invalid Input", "Please enter a valid YouTube URL.")
        return

    try:
        video = YouTube(video_url, on_progress_callback=progress_function)
    except PytubeError as e:
        messagebox.showinfo("Error", f"An error occurred: {str(e)}")
        return

    destination = filedialog.askdirectory()

    try:
        if var.get() == 'Audio':
            audio = video.streams.get_audio_only()
            output = audio.download(output_path=destination)
            base, ext = os.path.splitext(output)
            file = base + ".mp3"
            os.rename(output, file)
        elif var.get() == 'Video':
            if quality_var.get() == 'High':
                video_stream = video.streams.get_highest_resolution()
            elif quality_var.get() == 'Low':
                video_stream = video.streams.get_lowest_resolution()
            video_stream.download(output_path=destination)

    except Exception as e:
        messagebox.showinfo("Error", f"An error occurred: {str(e)}")
        return

    url_entry.delete(0, tk.END)
    messagebox.showinfo("Success", f"{video.title}'s {var.get()} is downloaded to {destination}")
    download_bar['value'] = 0

root = tk.Tk()
root.geometry('400x300')
root.title("MusicDownloader")

tk.Label(root, text="Youtube URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

var = tk.StringVar(root)
var.set("Audio")  # initial value

option = tk.OptionMenu(root, var, "Audio", "Video")
option.pack()

quality_var = tk.StringVar(root)
quality_var.set("High")  # initial value

quality_option = tk.OptionMenu(root, quality_var, "High", "Low")
quality_option.pack()

download_button = tk.Button(root, text="Download", command=download_media)
download_button.pack()

download_bar = ttk.Progressbar(root, length=400, mode='determinate')
download_bar.pack(pady=10)

root.mainloop()