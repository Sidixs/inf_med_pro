import os

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

from infmedsteg.forms import MessageForm
from infmedsteg.models import ClearFiles, Encoded
import wave
import struct

def allFiles(request):
    files = ClearFiles.objects.all()
    return render(request, 'allfiles.html',{'files':files})

def choosenFile(request, Fid):
    currentFile = ClearFiles.objects.get(id=Fid)

    if request.method == "POST":
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            message = messageForm.cleaned_data['message']
            print(message)
            file = currentFile.file
            song = wave.open(file, mode='rb')
            # Read frames and convert to byte array
            frame_bytes = bytearray(list(song.readframes(song.getnframes())))

            # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
            message = message + int((len(frame_bytes) - (len(message) * 8 * 8)) / 8) * '#'
            # Convert text to bit array
            bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))

            # Replace LSB of each byte of the audio data by one bit from the text bit array
            for i, bit in enumerate(bits):
                frame_bytes[i] = (frame_bytes[i] & 254) | bit
            frame_modified = bytes(frame_bytes)

            # Write bytes to a new wave audio file
            print(currentFile.file.url)
            out = Encoded()
            new_file = ContentFile(currentFile.file.read())
            print("current ",os.path.basename(currentFile.file.name))
            new_file.name=os.path.basename(currentFile.file.name)
            out.file = new_file
            out.name=messageForm.cleaned_data['title']
            out.auth_user_id=request.user.id
            out.save()
            print(out.file)
            out1 = Encoded.objects.filter(auth_user_id=request.user.id).order_by('-id')
            print(out1[0].file.path)
            with wave.open(out1[0].file.path, 'wb') as fd:
                fd.setparams(song.getparams())
                fd.writeframes(frame_modified)
            song.close()
            return redirect('myfiles')

    messageForm = MessageForm()
    return render(request, 'choosenfile.html',{'currentFile':currentFile, 'messageForm':messageForm})
