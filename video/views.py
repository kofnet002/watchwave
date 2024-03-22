from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VideoSerializer
import ffmpeg
import os
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config
from .models import Video

if not config('CLOUDINARY_API_SECRET'):
    raise Exception('CLOUDINARY_API_SECRET environment variable is not set.')

cloudinary.config(
  cloud_name = config('CLOUDINARY_CLOUD_NAME'),
  api_key = config('CLOUDINARY_API_KEY'),
  api_secret = config('CLOUDINARY_API_SECRET'),
  secure = True,
)



class VideoView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        video_serializer = VideoSerializer(videos, many=True)
        if video_serializer:
            return Response({
                'success': True,
                'data': video_serializer.data
            })
        return Response({
            'success': False,
            'data': video_serializer.errors
        })
    

    def post(self, request):
        if request.method == "POST":

            form_serializer = VideoSerializer(data=request.data)

            if form_serializer.is_valid():
                video_title = form_serializer.validated_data['title']
                video_description = form_serializer.validated_data['description']

                # Check if the title already exists
                if Video.objects.filter(title=video_title).exists():
                    return Response({'detail': "A video with this title already exists."}, status=400)

                # Check if the description already exists
                if Video.objects.filter(description=video_description).exists():
                    return Response({'detail': "A video with this description already exists."}, status=400)

                if request.data.get('video') is None:
                    return Response({'detail': "Please upload a video."}, status=400)
                
                video_file = request.data.get('video')

                # Check if the uploaded file is a video
                if not self.is_video_file(video_file):
                    return Response({'detail': "Uploaded file is not a valid video."}, status=400)

                fs = FileSystemStorage()
                filename = fs.save(video_file.name, video_file)
                input_path = fs.path(filename)

                name, ext = os.path.splitext(filename)
                output_path = fs.path(name + "_preview" + ext)

                try:
                    # trimmed_duration = self.get_trimmed_video_duration(input_path)
                    # self.trim_video(input_path, output_path, trimmed_duration)
                    full_video_url = self.upload_to_cloudinary(video_file, video_title)
                    # preview_video_url = self.upload_to_cloudinary(output_path, f"{video_title}_preview", is_file_path=True)

                    video_data = {
                        'title': video_title,
                        'description': video_description,
                        'video_url': full_video_url  # Use the Cloudinary URL here
                    }

                    video_instance = Video.objects.create(**video_data)
                    video_instance.save()

                    self.print_debug_info(full_video_url)
                    # self.print_debug_info(preview_video_url)

                    return Response({
                        'success': True,
                        'detail': "Video uploaded successfully."}, status=201)

                except Exception as e:
                    print(e, file=sys.stderr)
                    fs.delete(filename)
                    return Response({'detail': "An error occurred while processing the video."}, status=500)
                finally:
                    self.cleanup_files(fs, filename, output_path)

            else:
                return Response(form_serializer.errors, status=400)


     # Add a method to check if the uploaded file is a video
    def is_video_file(self, file):
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']
        _, ext = os.path.splitext(file.name)
        return ext.lower() in video_extensions
    
    # def get_trimmed_video_duration(self, input_path):
    #     video_info = ffmpeg.probe(input_path)
    #     duration = float(video_info['streams'][0]['duration'])
    #     return duration / 3


    # def trim_video(self, input_path, output_path, trimmed_duration):
    #     ffmpeg.input(input_path).output(output_path, t=trimmed_duration).run(overwrite_output=True)


    def upload_to_cloudinary(self, file, public_id, is_file_path=False):
        if is_file_path:
            with open(file, 'rb') as video_file:
                res = cloudinary.uploader.upload_large(video_file, 
                    resource_type="video",
                    public_id=public_id)

        else:
            res = cloudinary.uploader.upload_large(file, 
                resource_type="video",
                public_id=public_id)
            
        print('res', res)
        return res['secure_url']


    def print_debug_info(self, url):
        print("*" * 20)
        print(url)
        print("*" * 20)


    def cleanup_files(self, fs, *file_paths):
        for path in file_paths:
            fs.delete(path)
    
# def detail(request, video_id):
#     video = get_object_or_404(Video, pk=video_id)
#     return render(request, 'videos/index.html', {'video': video})

