from pytube import Playlist
from pytube import YouTube
from threading import Thread

import customtkinter
import os

WIDTH, HEIGHT = 450, 275
APP_NAME = "TubeLoader"

mode = 'Video' # Two modes: Video and Playlist

download_playlist_button = None
download_video_button = None
single_title = None
single_button = None
single_entry = None
info_text = None

def main():

    global download_playlist_button, download_video_button, mode, single_title, single_button, single_entry, info_text

    app = customtkinter.CTk()
    app.geometry(f'{WIDTH}x{HEIGHT}')
    app.title(APP_NAME)
    app.resizable(False, False)

    customtkinter.set_appearance_mode('light')

    title_font = customtkinter.CTkFont(family='fonts/Gilroy-Semibold',size=25)
    regular_font = customtkinter.CTkFont(family='fonts/Roboto-Regular',size=14)
    
    title = customtkinter.CTkLabel(app,
                                   text=APP_NAME,
                                   font=title_font,
                                   height=80)
    
    download_video_button = customtkinter.CTkButton(app,
                                                    width=100,
                                                    height=30,
                                                    text='Download video',
                                                    font=regular_font)
    download_playlist_button = customtkinter.CTkButton(app,
                                                       width=100,
                                                       height=30,
                                                       text='Download playlist',
                                                       font=regular_font)
    
    
    # Download single video
    single_title = customtkinter.CTkLabel(app,
                                          text='Just paste video URL')
    single_entry = customtkinter.CTkEntry(app,
                                          placeholder_text='URL',
                                          width=250)
    single_button = customtkinter.CTkButton(app,
                                            text='Download video',
                                            command=lambda: Thread(target=download_video).start())
    
    info_text = customtkinter.CTkLabel(app,
                                        text=None)
    
    download_playlist_button.configure(command=on_download_playlist_clicked)
    download_video_button.configure(command=on_download_video_clicked)

    download_video_button.place(x=WIDTH//2 - 70, y=HEIGHT//2 - 44, anchor='c')
    download_playlist_button.place(x=WIDTH//2 + 70, y=HEIGHT//2 - 44, anchor='c')
    single_title.place(x=WIDTH//2 - 65, y=HEIGHT//2, anchor='c')
    single_button.place(x=WIDTH//2, y=HEIGHT//2 + 70, anchor='c')
    single_entry.place(x=WIDTH//2, y=HEIGHT//2 + 30, anchor='c')
    info_text.place(x=WIDTH//2, y=HEIGHT//2 + 110, anchor='c')

    title.pack(anchor='c')

    if mode == 'Video':
        download_video_button.configure(state='disabled')
    else:
        download_playlist_button.configure(state='disabled')

    app.mainloop()


def on_download_playlist_clicked():
    global mode
    mode = 'Playlist'
    download_playlist_button.configure(state='disabled')
    download_video_button.configure(state='normal')
    single_title.configure(text='Just paste playlist URL')
    single_button.configure(text='Download playlist')
    
def on_download_video_clicked():
    global mode
    mode = 'Video'
    download_video_button.configure(state='disabled')
    download_playlist_button.configure(state='normal')
    single_title.configure(text='Just paste video URL')
    single_button.configure(text='Download video')

def download_video():
    link = single_entry.get()
    path = os.path.join(os.getcwd(), "videos")

    if mode == "Video" and link != "":
        try:
            single_button.configure(state='disabled')
            info_text.configure(text="Your video is downloading..")
            YouTube(single_entry.get()).streams.get_highest_resolution().download(output_path=path)
            
            # Print success information
            info_text.configure(text="Video downloaded successfully!")
            single_button.configure(state='normal')

        except Exception:
            info_text.configure(text="Link is invalid")
            single_button.configure(state='normal')

    elif mode == "Playlist" and link != "":
        try:   
            # Download notice
            info_text.configure(text="Your playlist is downloading..")
            single_button.configure(state='disabled')

            playlist = Playlist(single_entry.get())

            for video in playlist.videos:
                video.streams.get_highest_resolution().download(output_path=path)

            # Print success information
            info_text.configure(text="Playlist downloaded successfully!")
            single_button.configure(state='normal')

        except Exception:
            info_text.configure(text="Link is not playlist or invalid")
            single_button.configure(state='normal')

    if link == "":
        info_text.configure(text="Link input is empty")



if __name__ == "__main__":
    main()