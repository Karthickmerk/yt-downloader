from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix import Playlist
from pytubefix import Channel
from moviepy.editor import VideoFileClip, AudioFileClip
import ffmpeg


class ytDownload:
    def __init__(self, url, forceAudio):
        self.url = url
        self.forceAudio = forceAudio
        self.yt = YouTube(self.url, on_progress_callback = on_progress)

    def audioOnly(self):
        
        print(self.yt.title)
        ys = self.yt.streams.get_audio_only()
        return ys.download(mp3=True)
    
    def video(self):
        
        print(self.yt.title)
        ys = self.yt.streams.get_highest_resolution(progressive=False)
        videopath = ys.download()
        video = VideoFileClip(videopath)
        if video.audio is None and self.forceAudio:
            audioPath = self.audioOnly()
            audio = AudioFileClip(audioPath)
            newPath = videopath.replace('.mp4', '_merged.mp4')
            final_video = video.set_audio(audio)
            final_video.write_videofile(newPath, codec="libx264", audio_codec="aac")
            # ffmpeg.output(ffmpeg.input(video_input), ffmpeg.input(audio_input), output_file, vcodec='copy', acodec='aac').run()


    def audioPlayList(self):
        pl = Playlist(self.url)
        for video in pl.videos:
            ys = video.streams.get_audio_only()
            ys.download(mp3=True)
    
    def downloadChannel(self):
        c = Channel(self.url)
        print(f'Downloading videos by: {c.channel_name}')

        for video in c.videos:
            video.streams.get_highest_resolution().download()

    



youtubeDownload = ytDownload('https://www.youtube.com/watch?v=i_VM7WC1Yqo', True)
youtubeDownload.video()