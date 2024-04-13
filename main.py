from flask import Flask, request, jsonify
import tabula

app = Flask(__name__)

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    # Get the PDF file from the request
    file = request.files['pdf']

    # Read the PDF file
    tables = tabula.read_pdf(file, pages='all')

    # Process the tables and extract the desired data
    extracted_partnum = []
    extracted_partdes = []
    for df in tables:
        part_numbers = df['Part Number'].tolist()
        part_designations = df['Part Designation'].tolist()
        extracted_partnum.extend(part_numbers)  # Append individual part numbers
        extracted_partdes.extend(part_designations)  # Append individual part designations

    return jsonify({'Part Numbers': extracted_partnum, 'Part Designations': extracted_partdes})

if __name__ == '__main__':
    app.run(debug=True)
