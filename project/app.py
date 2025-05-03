from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfMerger
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist('pdfs')
    if not files or len(files) < 2:
        return "Please upload at least two PDF files.", 400

    merger = PdfMerger()
    for file in files:
        if file.filename.endswith('.pdf'):
            merger.append(file.stream)

    output = BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='merged.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
