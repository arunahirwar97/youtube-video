# from django.shortcuts import render, redirect
# from pytube import YouTube
# import os

# from django.http import FileResponse
# # Create your views here.
# def index(request):
#     homedir = os.path.expanduser("~")
#     dirs = homedir + "/Downloads/"
#     print("outside loop")
#     if request.method == 'POST':
#         link = request.POST.get("youtubeLink")
#         print(link)
#         return FileResponse(open(YouTube(link).streams.filter(type = "audio").first().download(),'rb'))	
#     return render(request, 'index.html')

from django.shortcuts import render, redirect
from pytube import YouTube
import os
from django.http import FileResponse


# Create your views here.
def index(request):
    # homedir = os.path.expanduser("~")
    # dirs = homedir + "/Downloads/"

    # if request.method == 'POST':
    #     link = request.POST.get("youtubeLink")
    #     downloadAudio = request.POST.get("downloadAudio")
    #     downloadVideo = request.POST.get("downloadVideo")
    #     audioQuality = request.POST.get("AudioQuality")
    #     videoQuality = request.POST.get("VideoQuality")

    #     if link:
    #         yt = YouTube(link)
    #         title = yt.title
    #         thumbnail = yt.thumbnail_url

    #         audio = []
    #         audio_size = []
    #         video = []
    #         video_size = []
    #         for i in yt.streams.filter(only_audio=True):
    #             print(i)
    #             audio.append(i.abr)
    #             size = i.filesize / (1024 * 1024)
    #             size = round(size, 2)
    #             audio_size.append(size)
    #         for j in yt.streams.filter(only_video=True, mime_type="video/mp4"):
    #             video.append(j.resolution)
    #             size = j.filesize / (1024 * 1024)
    #             size = round(size, 2)
    #             video_size.append(size)
    #         audio.sort()
    #         video = list(set(video))
    #         video.sort()
    #         return render(request, 'index.html', {
    #             'thumbnail': thumbnail,
    #             'title': title,
    #             'audio': zip(audio, audio_size),
    #             'video': zip(video, video_size),
    #             'link': link,
    #         })
    #     elif downloadAudio:
    #         if audioQuality != "Audio Quality" and downloadAudio is not None:
    #             yt = YouTube(downloadAudio)
    #             yt = yt.streams.filter(abr=audioQuality)
    #             return FileResponse(open(yt.first().download(), 'rb'))
    #         else:
    #             print("select audio quality")
    #             return render(request, 'index.html', {
    #                 'error': "Choose Audio Quality",
    #             })
    #     elif downloadVideo:
    #         if videoQuality != "Video Quality" and downloadVideo is not None:
    #             print("Download")
    #             yt = YouTube(downloadVideo)
    #             print(videoQuality)
    #             yt = yt.streams.filter(res=videoQuality, mime_type="video/mp4")
    #             return FileResponse(open(YouTube('https://www.youtube.com/watch?v=J0fI57tE4aI').streams.filter(res="360p").first().download(), 'rb'))
    #         else:
    #             print("select video quality")
    #             return render(request, 'index.html', {
    #                 'error': "Choose Video Quality",
    #             })
    #     else:
    #         return render(request, 'index.html', {
    #             'error': "Enter a correct URL",
    #         })
    return FileResponse(open(YouTube('https://www.youtube.com/watch?v=J0fI57tE4aI').streams.filter(res="360p").first().download(), 'rb'))

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from .forms import DownloadForm
import re


def download_video(request):
    global context
    form = DownloadForm(request.POST or None)
    
    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        if not re.match(regex,video_url):
            return HttpResponse('Enter correct url.')

        ydl_opts = {}
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    video_url, download=False)
            video_audio_streams = []
            for m in meta['formats']:
                file_size = m['filesize']
                if file_size is not None:
                    file_size = f'{round(int(file_size) / 1000000,2)} mb'

                resolution = 'Audio'
                if m['height'] is not None:
                    resolution = f"{m['height']}x{m['width']}"
                video_audio_streams.append({
                    'resolution': resolution,
                    'extension': m['ext'],
                    'file_size': file_size,
                    'video_url': m['url']
                })
            video_audio_streams = video_audio_streams[::-1]
            context = {
                'form': form,
                'title': meta.get('title', None),
                'streams': video_audio_streams,
                'description': meta.get('description'),
                'likes': f'{int(meta.get("like_count", 0)):,}',
                'dislikes': f'{int(meta.get("dislike_count", 0)):,}',
                'thumb': meta.get('thumbnails')[3]['url'],
                'duration': round(int(meta.get('duration', 1))/60, 2),
                'views': f'{int(meta.get("view_count")):,}'
            }
            return render(request, 'home.html', context)
        except Exception as error:
            return HttpResponse(error.args[0])
    return render(request, 'home.html', {'form': form})
