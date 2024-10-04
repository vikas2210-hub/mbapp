from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

# Function to compress the image forcefully to 15 KB
def compress_image(image, format, target_size=15 * 1024):
    quality = 85  # Start with high quality
    img_bytes = io.BytesIO()
    
    # Try different qualities until the image size is <= 15 KB
    while True:
        img_bytes.seek(0)
        image.save(img_bytes, format=format, quality=quality)
        size = img_bytes.tell()
        
        if size <= target_size or quality <= 5:  # Stop when it's <= 15 KB or quality is too low
            break
        quality -= 5  # Reduce quality incrementally
    
    img_bytes.seek(0)
    return img_bytes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image uploaded", 400

    file = request.files['image']
    format = request.form.get('format', 'JPEG')  # Choose format from the form (JPEG, PNG, WebP)
    
    # Open the image using PIL
    image = Image.open(file)
    
    # Compress the image forcefully to 15 KB
    compressed_image = compress_image(image, format)

    # Set appropriate file extension and MIME type
    extension = format.lower()
    mime_type = f'image/{extension}'

    # Return the compressed image as a downloadable file
    return send_file(compressed_image, mimetype=mime_type, as_attachment=True, download_name=f"compressed.{extension}")

if __name__ == '__main__':
    app.run(debug=True)
