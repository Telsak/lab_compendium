from flask import (
    Flask, request, render_template, jsonify, send_from_directory, url_for,
    Response, stream_with_context
    )
from pdfmagic import build_even_labfile, build_lab_compendium, convert_docx_to_pdf
from pathlib import Path
import uuid

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

app = Flask(__name__)

UPLOAD_FOLDER = Path('C:/Temp/pdfstuff')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    unique_id = str(uuid.uuid4())
    upload_folder = UPLOAD_FOLDER / unique_id

    if not upload_folder.exists():
        if not upload_folder.exists():
            upload_folder.mkdir(parents=True, exist_ok=True)
            (upload_folder / 'out').mkdir(parents=True, exist_ok=True)
            (upload_folder / 'docx').mkdir(parents=True, exist_ok=True)
    
    uploaded_files = request.files.getlist("files")
    counter = 0
    num_files = len(uploaded_files)
    print(counter, num_files)
    for file in uploaded_files:
        if file:
            filepath = upload_folder / file.filename
            if file.filename.endswith('.docx'):
                file.save(upload_folder / 'docx' / file.filename)
                convert_docx_to_pdf(upload_folder, file.filename)
                file.filename = file.filename[:-5]+'.pdf'
            elif file.filename.endswith('.pdf'):
                file.save(filepath)
            build_even_labfile(UPLOAD_FOLDER, unique_id, file.filename)

    if build_lab_compendium(UPLOAD_FOLDER, unique_id):
        success_url = url_for('download_file', unique_id=unique_id)
        return jsonify({'success_url': success_url})
    else:
        # Handle the error case
        return jsonify({'error': 'Failed to create compendium'})

@app.route('/download/<unique_id>', methods=['GET'])
def download_file(unique_id):
    directory = UPLOAD_FOLDER / unique_id / 'out'
    filename = 'lab_compendium.pdf'
    file_path = directory / filename

    # Check if the file exists
    if not file_path.exists():
        return "Error: File not found", 404

    # If the file exists, send it from the directory
    return send_from_directory(str(directory), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
