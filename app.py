from flask import Flask, request, jsonify, send_file,render_template
import cv2
import numpy as np
import io

app = Flask(__name__)


def resize_image(image, width, height):
    # Perform the resize operation
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    return resized_image


@app.route('/')
def index():
    return render_template("image_resize_index.html")


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    try:
        width = int(request.form['width'])
        height = int(request.form['height'])
    except ValueError:
        return "Invalid width or height", 400

    # Convert the uploaded file to a NumPy array
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return "Invalid image file", 400

    # Resize the image
    resized_image = resize_image(image, width, height)
    print(resized_image)

    # Convert the resized image to byte array for sending as response
    _, buffer = cv2.imencode('.jpg', resized_image)
    byte_io = io.BytesIO(buffer)

    # Send the resized image as response
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)
