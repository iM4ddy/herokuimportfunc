import os

from flask import Flask, request, jsonify
import tabula

app = Flask(__name__)

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    # Check if a file is present in the request
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf']

    # Check if the file name is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is a PDF
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File is not a PDF'}), 400

    # Read the PDF file
    try:
        tables = tabula.read_pdf(file, pages='all')
    except Exception as e:
        return jsonify({'error': 'Failed to read PDF', 'details': str(e)}), 500

    # Process the tables and extract the desired data
    extracted_partnum = []
    extracted_partdes = []
    for df in tables:
        part_numbers = df.get('Part Number', [])  # Use get() to handle missing columns
        part_designations = df.get('Part Designation', [])  # Use get() to handle missing columns
        extracted_partnum.extend(part_numbers)
        extracted_partdes.extend(part_designations)

    return jsonify({'Part Numbers': extracted_partnum, 'Part Designations': extracted_partdes})

@app.route('/home')
def home_page():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
