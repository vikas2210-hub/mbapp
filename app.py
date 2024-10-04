from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

def compress_image(image, format, target_size=15 * 1024):
    """Compress the image to exactly 15 KB."""
    quality = 100  # Start with the best quality
    img_byte_arr = io.BytesIO()

    # Keep compressing until the image reaches the target size
    while True:
        img_byte_arr.seek(0)
        image.save(img_byte_arr, format=format, quality=quality)
        img_size = img_byte_arr.tell()

        if img_size <= target_size or quality <= 5:
            break
        quality -= 5  # Reduce the quality to shrink the image

    img_byte_arr.seek(0)
    return img_byte_arr

@app.route('/resize', methods=['POST'])
def resize_image():
    file = request.files['image']
    format = request.form['format']
    image = Image.open(file)

    # Compress the image to 15 KB
    img_byte_arr = compress_image(image, format.upper())

    return send_file(
        io.BytesIO(img_byte_arr.read()),
        mimetype=f'image/{format}',
        as_attachment=True,
        download_name=f'resized.{format}'
    )

if __name__ == '__main__':
    app.run(debug=True)
