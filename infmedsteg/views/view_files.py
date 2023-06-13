import os

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

from infmedsteg.forms import MessageForm
from infmedsteg.models import ClearFiles, Encoded
import wave

@login_required
def allFiles(request):
    files = ClearFiles.objects.all()
    return render(request, 'allfiles.html',{'files':files})

@login_required
def choosenFile(request, Fid):
    currentFile = ClearFiles.objects.get(id=Fid)

    if request.method == "POST":
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            message = messageForm.cleaned_data['message']
            file = currentFile.file
            song = wave.open(file, mode='rb')
            frame_bytes = bytearray(list(song.readframes(song.getnframes())))
            message = message + int((len(frame_bytes) - (len(message) * 8 * 8)) / 8) * '#'
            bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))
            for i, bit in enumerate(bits):
                frame_bytes[i] = (frame_bytes[i] & 254) | bit
            frame_modified = bytes(frame_bytes)
            out = Encoded()
            new_file = ContentFile(currentFile.file.read())
            new_file.name=os.path.basename(currentFile.file.name)
            out.file = new_file
            out.name=messageForm.cleaned_data['title']
            out.auth_user_id=request.user.id
            out.save()
            out1 = Encoded.objects.filter(auth_user_id=request.user.id).order_by('-id')
            with wave.open(out1[0].file.path, 'wb') as fd:
                fd.setparams(song.getparams())
                fd.writeframes(frame_modified)
            song.close()
            return redirect('myfiles')

    messageForm = MessageForm()
    return render(request, 'choosenfile.html',{'currentFile':currentFile, 'messageForm':messageForm})
