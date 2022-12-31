import os
from flask import Flask, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the upload directory and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def chat():
    messages = []  # Initialize the messages list
    if request.method == 'POST':
        # Get the message and image (if any) from the form
        message = request.form['message']
        image = request.files['image']

        # Save the image (if any) to the uploads folder
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f"/{UPLOAD_FOLDER}/{filename}"
        else:
            image_url = None

        # Append the message and image URL to the messages list
        messages.append((message, image_url))

    # Render the chat template
    return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    app.run()
