from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfMerger

# Directories for uploads and merged files
UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'

# Create folders if they do not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Configure app with upload and merged file paths
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')  # Rendering the HTML from the templates folder

@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist('pdfs')
    if not files:
        return redirect(url_for('index'))  # If no files are uploaded, go back to the home page

    merger = PdfMerger()
    uploaded_files = []

    # Save the uploaded files and add them to the merger
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        uploaded_files.append(filepath)
        merger.append(filepath)

    # Create merged file
    merged_filename = 'merged.pdf'
    merged_path = os.path.join(app.config['MERGED_FOLDER'], merged_filename)
    merger.write(merged_path)
    merger.close()

    # Clean up the uploaded files
    for f in uploaded_files:
        os.remove(f)

    return send_file(merged_path, as_attachment=True)  # Send the merged PDF file as download

if __name__ == '__main__':
    # Remove app.run() for production, you will use Gunicorn or similar for deployment
    # app.run(debug=True)  # This can be removed or replaced by a production WSGI server (like Gunicorn)
