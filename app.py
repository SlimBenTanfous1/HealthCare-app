from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file.save(f"uploads/{file.filename}")
        return f"File {file.filename} uploaded successfully!"
    return "No file selected"



if __name__ == "__main__":
    import os

    # Only enable debug if explicitly set via environment variable
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)
