from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfMerger

UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist('pdfs')
    if not files:
        return redirect(url_for('index'))

    merger = PdfMerger()
    uploaded_files = []

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        uploaded_files.append(filepath)
        merger.append(filepath)

    merged_filename = 'merged.pdf'
    merged_path = os.path.join(app.config['MERGED_FOLDER'], merged_filename)
    merger.write(merged_path)
    merger.close()

    # Clean up uploaded files
    for f in uploaded_files:
        os.remove(f)

    return send_file(merged_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
