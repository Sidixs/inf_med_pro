import wave

from django.shortcuts import render, redirect

from infmedsteg.models import Encoded


def allEncoded(request):
    files = Encoded.objects.filter(auth_user_id=request.user.id)
    return render(request, 'allencoded.html',{'files':files})

def choosenEncoded(request, Fid):
    currentFile = Encoded.objects.get(id=Fid)
    decoded = ''
    if request.method == "POST":
        if 'delete' in request.POST:
            currentFile.delete()
            return redirect('myfiles')
        if 'decode' in request.POST:
            file = currentFile.file
            print(file.path)
            song = wave.open(file.path, mode='rb')
            # Convert audio to byte array
            frame_bytes = bytearray(list(song.readframes(song.getnframes())))
            # Extract the LSB of each byte
            extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            # Convert byte array back to string
            message = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
            # Cut off at the filler characters
            decoded = message.split("###")[0]
            song.close()


    return render(request, 'choosenencoded.html',{'currentFile':currentFile,'decoded':decoded})