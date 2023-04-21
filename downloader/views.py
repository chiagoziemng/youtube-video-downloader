import os
from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube

def download_video(request):
    if request.method == 'POST':
        # Get the URL and desired format from the form
        url = request.POST.get('url')
        format = request.POST.get('format')

        # Download the video
        try:
            yt = YouTube(url)
            video = yt.streams.filter(file_extension=format).first()
            if not video:
                return render(request, 'error.html', {'message': 'Video could not be downloaded'})

            # Get the user's download directory
            download_dir = request.POST.get('download_dir', os.path.expanduser("~/Downloads"))

            # Save the video to the user's download directory
            video_path = os.path.join(download_dir, f'{yt.title.replace("/", "_")}.{format}')
            video.download(output_path=download_dir, filename=yt.title)

            # Return the downloaded video to the user
            with open(video_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.{format}"'
            
              # Render the success message template
            return render(request, 'success.html', {'message': 'Video downloaded successfully'})


        except Exception as e:
            return render(request, 'error.html', {'message': str(e)})

    # Render the form template if the request method is GET
    return render(request, 'download.html')
