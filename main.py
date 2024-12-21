import tkinter as tk
from tkinter import messagebox
import os
import yt_dlp

def download_video(url_entry, audio_only_var):
    url = url_entry.get()
    save_path = os.path.join(os.path.expanduser("~"), "Downloads")

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    try:
        if audio_only_var.get():
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.mp3'),  # Force .mp3 extension
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.mp4'),  # Force .mp4 extension
                'format': 'bestvideo+bestaudio',  # Download both video and audio
                'merge_output_format': 'mp4',    # Merge into an MP4 file
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }, {
                    'key': 'FFmpegMetadata',  # Ensure audio is AAC
                }, {
                    'key': 'FFmpegEmbedSubtitle',  # Handle subtitles if available
                }],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f"Video downloaded successfully to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    root.title("YouTube Video Downloader")
    root.geometry("500x250")
    root.configure(bg="#CECECE")

    # URL label and entry
    url_label = tk.Label(root, text="YouTube URL:")
    url_label.pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=10)

    # Audio-only checkbox
    audio_only_var = tk.BooleanVar()
    audio_only_checkbox = tk.Checkbutton(root, text="Download audio only (MP3)", variable=audio_only_var)
    audio_only_checkbox.pack(pady=10)

    # Download button
    download_button = tk.Button(root, text="Download", command=lambda: download_video(url_entry, audio_only_var))
    download_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()