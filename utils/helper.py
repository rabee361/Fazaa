from datetime import timedelta
from django.utils import timezone
import random
import os
from django.core.files.base import ContentFile
import io
from django.conf import settings
from moviepy import VideoFileClip
from PIL import Image


def get_expiration_time():
    return timezone.now() + timedelta(minutes=10)

def generate_code():
    code = random.randint(1000,9999)
    return code

def generateShortUrl():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random_string = ''.join(random.choice(letters) for _ in range(8))
    return random_string

def generate_product_deep_link(organization):
    # Use your actual app scheme instead of "fazaaapp"
    app_scheme = "fazaa"
    resource_type = "organizations"
    resource_id = str(organization.id)
    
    return f"{app_scheme}://{resource_type}/{resource_id}"


def getRandomPhonenumber():
    return '01' + str(random.randint(100000000,999999999))

def getRandomEmail():
    return 'test' + str(random.randint(100000000,999999999)) + '@test.com'

def getRandomPassword():
    return 'rabee123@@123'

def generate_video_thumbnail(video_path):
    """
    Generate a JPEG thumbnail for a video by extracting the first frame as a JPEG image.
    Returns the relative path to the thumbnail file.
    Uses moviepy (a lightweight library) instead of ffmpeg directly.
    """

    # Ensure the video exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Prepare thumbnail filename and path (JPEG format)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    thumb_filename = f"{base_name}_thumb.jpeg"
    thumb_dir = os.path.join(settings.MEDIA_ROOT, 'images', 'thumbnails')
    os.makedirs(thumb_dir, exist_ok=True)
    thumb_path = os.path.join(thumb_dir, thumb_filename)

    try:
        # Load the video and get the first frame
        with VideoFileClip(video_path) as clip:
            frame = clip.get_frame(0)  # Get the first frame (at t=0)
            img = Image.fromarray(frame)
            img = img.convert("RGB")
            img.thumbnail((300, 300))  # Optional: resize thumbnail
            img.save(thumb_path, "JPEG", quality=85)
    except Exception as e:
        print(f"Error generating video thumbnail: {e}")
        return None

    # Return the relative path from MEDIA_ROOT for Django ImageField
    rel_thumb_path = os.path.relpath(thumb_path, settings.MEDIA_ROOT)
    return os.path.join(rel_thumb_path).replace("\\", "/")

    
def generate_img_thumbnail(image_path):
    try:
        print(f"Starting thumbnail generation for image: {image_path}")
        
        # Convert Django path to real file system path
        if os.path.isabs(image_path) and os.path.exists(image_path):
            real_path = image_path
        else:
            # If it's a relative path from MEDIA_ROOT, construct the absolute path
            relative_path = image_path.replace('media/', '', 1) if image_path.startswith('media/') else image_path
            real_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            print(f"Converted path to: {real_path}")
        
        # Verify image file exists
        if not os.path.exists(real_path):
            print(f"Image file not found at path: {real_path}")
            raise FileNotFoundError(f"Image file not found: {real_path}")
            
        # Create thumbnails directory if it doesn't exist
        thumb_dir = os.path.join(settings.MEDIA_ROOT, 'images/thumbnails/')
        print(f"Creating thumbnails directory at: {thumb_dir}")
        os.makedirs(thumb_dir, exist_ok=True)
        
        # Create thumbnail file path
        thumb_filename = os.path.splitext(os.path.basename(real_path))[0] + '_thumb.jpg'
        thumb_path = os.path.join(thumb_dir, thumb_filename)
        print(f"Thumbnail will be saved as: {thumb_filename}")

        # Open the image and create a thumbnail
        print("Opening image and creating thumbnail...")
        with Image.open(real_path) as img:
            # Convert to RGB if image is in RGBA mode (for PNG transparency)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                # Paste the image on the background if it has alpha
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
                
            print(f"Original image size: {img.size}")
            # Keep aspect ratio
            img.thumbnail((300, 300))
            print(f"Thumbnail size: {img.size}")
            
            # Save to a buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            print("Image saved to buffer")
            
            # Create ContentFile from buffer
            content_file = ContentFile(buffer.getvalue())
            print("ContentFile created from buffer")
            
        print("Thumbnail generation completed successfully")
        return content_file, thumb_filename

    except Exception as e:
        print(f"Error generating thumbnail: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        raise
