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
        return FileResponse(open(YouTube(link).streams.filter(res='480p').first().download(),'rb'))	
    return render(request, 'index.html')


