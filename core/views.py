import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.conf import settings
from core.utiles import tool_zip_701


class Engine(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Assuming 'image' is the key for DICOM file in request.data
        dicom_file = request.FILES.get('image')
        
        if not dicom_file:
            return Response({"error": "No DICOM file provided."}, status=400)

        # Check if the file is a DICOM file
        if dicom_file.content_type != 'application/octet-stream':
            return Response({"error": "Please upload a DICOM file. Only DICOM files are supported."}, status=400)

        try:
            # Define the target directory where the DICOM file will be saved
            target_dir = os.path.join(settings.MEDIA_ROOT, 'temp', 'dicom')

            # Ensure the directory exists, create if not
            os.makedirs(target_dir, exist_ok=True)

            # Save the DICOM file to the target directory
            file_path = os.path.join(target_dir, dicom_file.name)
            
            with open(file_path, 'wb') as destination:
                for chunk in dicom_file.chunks():
                    destination.write(chunk)
            
            img_to_process = tool_zip_701(file_path)
            

            # Return success response
            return Response({"success": "DICOM file saved successfully.", "file_path": file_path}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
