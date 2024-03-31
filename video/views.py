from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VideoSerializer
import os
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .models import Video
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_field
import subprocess
import tempfile
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from supabase_py import create_client
from drf_spectacular.types import OpenApiTypes

# ... existing code ...

class VideoView(APIView):
    parser_classes = (FormParser, MultiPartParser, FileUploadParser)
    
    video_parameter = OpenApiParameter(
        name='page',
        location=OpenApiParameter.QUERY,
        description='A page number within the paginated result set.',
        type=OpenApiTypes.INT
        )
    @extend_schema(
            responses=VideoSerializer(many=True),
            tags=['Video'],
            summary='Get all videos',
            description='This endpoint returns all videos in the database.',
            parameters=[video_parameter]
            )
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = getattr(settings, 'PAGE_SIZE', 10)

        videos = Video.objects.order_by('id')  # Order the queryset by id
        result_page = paginator.paginate_queryset(videos, request)
        video_serializer = VideoSerializer(result_page, many=True)
        
        return paginator.get_paginated_response({
            'success': True,
            'data': video_serializer.data
        })
    

    @extend_schema(
            request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'title': {},
                    'description': {},
                    'video': {
                        'type': 'string',
                        'format': 'binary',
                        }
                    },
                'required': ['title', 'description', 'video'], 
                }
            },
            tags=['Video'],
            summary='Upload a video',
            description='This endpoint allows you to upload a video.', 
            responses={201: VideoSerializer},
            
            )
    
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
                        'detail': "Video uploaded successfully.",
                        'data': {
                            'id': video_instance.id,
                            'title': video_instance.title,
                            'description': video_instance.description,
                            'video_url': video_instance.video_url,
                            'created_at': video_instance.created_at,
                            'updated_at': video_instance.updated_at
                        }
                        }, status=201)

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
    

    def upload_to_cloudinary(self, file, filename, is_file_path=False):
        # Set up paths
        video_path = file if is_file_path else None
        path = f"videos/{filename}"  # Example path: videos/yourfilename
        public_id = f"{path}/{filename}"  # Example public_id: videos/yourfilename
        previews_path = f"{path}/previews/"  # Example path: videos/yourfilename/previews

        # Upload video to Cloudinary
        if is_file_path:
            with open(file, 'rb') as video_file:
                res = cloudinary.uploader.upload_large(video_file, 
                    resource_type="video",
                    public_id=public_id)
        else:
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                video_path = temp_file.name

            # Upload the temporary file to Cloudinary
            with open(video_path, 'rb') as temp_video_file:
                res = cloudinary.uploader.upload_large(temp_video_file, 
                    resource_type="video",
                    public_id=public_id)

        # Use ffmpeg to generate preview images
        output_folder = os.path.join(settings.MEDIA_ROOT, 'preview_images')
        os.makedirs(output_folder, exist_ok=True)
        subprocess.run([
            'ffmpeg',
            '-i', video_path,
            '-vf', 'fps=1/10 scale=120:-1', # Extract 1 frame per 10 seconds
            os.path.join(output_folder, 'image_%d.jpg')
        ])
        
        # Upload the preview images to Cloudinary
        image_files = sorted(os.listdir(output_folder))  # Sort image files by name
        for i, image_file in enumerate(image_files, start=1):
            image_path = os.path.join(output_folder, image_file)
            with open(image_path, 'rb') as image:
                image_public_id = f"{previews_path}/image_{i:d}"  # Format public_id
                response = cloudinary.uploader.upload(image,
                    public_id=image_public_id,
                    overwrite=True)
                # print('response******************)', response)
            
        # Delete the temporary files
        if not is_file_path:
            os.remove(video_path)        
        for image_file in image_files:
            os.remove(os.path.join(output_folder, image_file))
        os.rmdir(output_folder)  # Remove the output folder itself

        return res['secure_url']

    def print_debug_info(self, url):
        print("*" * 20)
        print(url)
        print("*" * 20)

    def cleanup_files(self, fs, *file_paths):
        for path in file_paths:
            fs.delete(path)

class SingleVideo(APIView):
    parser_classes = (FormParser, MultiPartParser, FileUploadParser)
    def get_object(self, id):
        try:
            return Video.objects.get(id=id)
        except Video.DoesNotExist:
            raise Response("Object not found")

    @extend_schema(
        responses=VideoSerializer,
        tags=['Video'],
        summary='Get a single video',
        description='This endpoint returns a single video by its ID.',
        )
    def get(self, request, id):
        video = self.get_object(id)
        all_videos = Video.objects.count()
        serializer = VideoSerializer(video)

         # Fetch the index of the current video
        current_video_index = Video.objects.filter(id__lte=id).count()

        data = {
            'id': serializer.data['id'],
            'title': serializer.data['title'],
            'description': serializer.data['description'],
            # 'video': serializer.data['video'],
            'video_url': serializer.data['video_url'],
            'current_index': current_video_index,
            'total_count': all_videos,
        }
        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
    
class NextVideoAPIView(APIView):
    parser_classes = (FormParser, MultiPartParser, FileUploadParser)

    @extend_schema(
            responses=VideoSerializer(many=True),
            tags=['Video'],
            summary='Get the next video in the queue',
            description='This endpoint returns the next videos in the queue.',
            )
    def get(self, request, current_video_id):
        try:
            # Fetch next video and count of all videos
            next_video = Video.objects.filter(id__gt=current_video_id).first()
            all_videos = Video.objects.count()

            if next_video:
                # Fetch the index of the current video
                current_video_index = Video.objects.filter(id__lte=current_video_id).count() + 1

                # Serialize the next video
                serializer = VideoSerializer(next_video)

                # Construct the response data
                data = {
                    'id': serializer.data['id'],
                    'title': serializer.data['title'],
                    'description': serializer.data['description'],
                    'video_url': serializer.data['video_url'],
                    'current_index': current_video_index,  # Add current video index
                    'total_count': all_videos,
                }
                return Response({'success': True, 'data': data})
            else:
                return Response({'success': False, 'detail': 'No next video'}, status=status.HTTP_404_NOT_FOUND)
        except (Video.DoesNotExist, ValueError):
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

class PreviousVideoAPIView(APIView):
    @extend_schema(
            responses=VideoSerializer(many=True),
            tags=['Video'],
            summary='Get the previous video in the queue',
            description='This endpoint returns the previous videos in the queue.',
            )
    def get(self, request, current_video_id):
        try:
            # Fetch previous video
            previous_video = Video.objects.filter(id__lt=current_video_id).last()

            if previous_video:
                # Fetch the index of the current video
                current_video_index = Video.objects.filter(id__lte=current_video_id).count() - 1

                # Serialize the previous video
                serializer = VideoSerializer(previous_video)

                # Construct the repsonse data
                data = {
                    'id': serializer.data['id'],
                    'title': serializer.data['title'],
                    'description': serializer.data['description'],
                    'video_url': serializer.data['video_url'],
                    'current_index': current_video_index,  # Add current video index
                }
                return Response({'success': True, 'data': data})
            else:
                return Response({'success': False, 'detail': 'No previous video'}, status=status.HTTP_404_NOT_FOUND)
        except (Video.DoesNotExist, ValueError):
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)