from django.shortcuts import render, redirect
from app.forms import FileUploadForm
from app.models.models1 import UploadedFile

def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # You can add code here for file verification
            return redirect('file_upload')
    else:
        form = FileUploadForm()
    return render(request, 'file_upload.html', {'form': form})


def list_uploads(request):
    uploaded_files = UploadedFile.objects.all()
    context = {
        'uploaded_files': uploaded_files,
    }
    return render(request, 'uploads_list.html', context)