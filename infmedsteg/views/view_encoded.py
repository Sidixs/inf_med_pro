import wave
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from infmedsteg.models import Encoded


@login_required
def allEncoded(request):
    files = Encoded.objects.filter(auth_user_id=request.user.id)
    return render(request, 'allencoded.html', {'files': files})


@login_required
def choosenEncoded(request, Fid):
    currentFile = Encoded.objects.get(id=Fid)
    decoded = ''
    if request.method == "POST":
        if 'delete' in request.POST:
            currentFile.delete()
            return redirect('myfiles')
        if 'decode' in request.POST:
            file = currentFile.file
            song = wave.open(file.path, mode='rb')
            frame_bytes = bytearray(list(song.readframes(song.getnframes())))
            extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            message = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
            decoded = message.split("###")[0]
            song.close()
    return render(request, 'choosenencoded.html', {'currentFile': currentFile, 'decoded': decoded})
