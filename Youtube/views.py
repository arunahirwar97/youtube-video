from django.shortcuts import render, redirect
from pytube import YouTube
import os

from django.http import FileResponse
# Create your views here.
def index(request):
    homedir = os.path.expanduser("~")
    dirs = homedir + "/Downloads/"
    print("outside loop")
    if request.method == 'POST':
        link = request.POST.get("youtubeLink")
        print(link)
        return FileResponse(open(YouTube('https://www.youtube.com/watch?v=jhFDyDgMVUI').streams.first().download(skip_existing=True),'rb'))	
    return render(request, 'index.html')
