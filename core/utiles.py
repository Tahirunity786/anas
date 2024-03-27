import pydicom
import numpy as np
from PIL import Image
from django.conf import settings
import os
import requests
from ultralytics import YOLO
import uuid
from time import sleep


model = YOLO(os.path.join(settings.BASE_DIR, 'model', 'best.pt'))

# Inference function
def image_processor(image_path, *args, **kwargs):
    results = model(image_path)

    for result in results:
        processed_image_path = os.path.join(settings.MEDIA_ROOT, 'model', 'product', f'{uuid.uuid4()}.jpeg')
        
        result.save(processed_image_path)
        
        retries = 3
        for attempt in range(retries):
            try:
                with open(processed_image_path, 'rb') as image_file:
                    files = {'file': image_file}
                    url = 'http://119.40.116.54:4342'
                    headers = {'AETitle': 'PADIDEMO'}
                    
                    response = requests.post(url, files=files, headers=headers)
                
                if response.status_code == 200:
                    print("Processed image uploaded successfully")
                    break
                else:
                    print(f"Failed to upload processed image. Status code: {response.status_code}")
            except ConnectionResetError as e:
                print(f"Connection reset error occurred: {e}. Retrying...")
                if attempt < retries - 1:
                    sleep(5)  # Wait for a few seconds before retrying
                else:
                    print("Maximum retry attempts reached.")


def tool_zip_701(image_path, *args, **kwargs):
    try:
        dicom_image = pydicom.dcmread(image_path)
        pixel_array = dicom_image.pixel_array

        # Ensure pixel_array has the correct shape (512, 512)
        if len(pixel_array.shape) != 2:
            raise ValueError("Invalid pixel array shape")

        # Convert pixel_array to unsigned 8-bit integer array (dtype=np.uint8)
        pixel_array = pixel_array.astype(np.uint8)

        # Rescale pixel values to [0, 255]
        rescaled_image = (pixel_array.astype(float) / np.max(pixel_array)) * 255

        # Convert to PIL Image
        image = Image.fromarray(rescaled_image)

        # Convert to RGB if the image is not already in RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Generate file name
        file_name = os.path.basename(image_path) + ".jpeg"
        
        # Define the target directory
        target_dir = os.path.join(settings.MEDIA_ROOT, "product")
        
        # Ensure the directory exists, create if not
        os.makedirs(target_dir, exist_ok=True)

        # Save the image as JPEG
        image_path = os.path.join(target_dir, file_name)
        image.save(image_path, 'JPEG')

        image_processor(image_path)
        # Return the path to the saved image
        return image_path
    
    except Exception as e:
        raise ValueError("Error processing DICOM file: {}".format(str(e)))

