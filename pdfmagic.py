from pypdf import PdfReader, PdfWriter
from pathlib import Path
import subprocess, sys

def build_even_labfile(path, unique_id, filename):
    base_path = Path(path) / unique_id
    pdf_file = PdfReader(base_path / filename)
    pdf_pages = len(pdf_file.pages)

    output_file = PdfWriter()
    output_file.append(str(base_path / filename))
    
    if pdf_pages % 2 == 1:
        # add a blank page here
        output_file.append(str(path / 'blank.pdf'))
    
    output_file.write(str(base_path / 'out' / filename))
    
    return True

def build_lab_compendium(path, unique_id):
    base_path = Path(path) / unique_id / 'out'
    output_file = PdfWriter()

    pdf_files = sorted(base_path.glob('*.pdf'))
    for pdf_path in pdf_files:
        output_file.append(str(pdf_path))
    
    output_file.write(str(base_path / 'lab_compendium.pdf'))
    return True

def convert_docx_to_pdf(upload_folder, filename):
    docx_folder = upload_folder / 'docx'
    pdf_folder = upload_folder
    soffice = Path('C:\Program Files\LibreOffice\program\soffice.exe')
    try:
        result = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", pdf_folder, docx_folder / filename])
        print('convert success')
    except:
        print('failed')