from flask import Flask, request, send_file
from flask_cors import CORS
from docxtpl import DocxTemplate
import os

app = Flask(__name__)
CORS(app)

# Path to your Word template (use Jinja-style {{ name }} placeholders in the file)
TEMPLATE_PATH = os.path.join('tempelates', 'contract_tempelate_1.docx') # Make sure this matches your real path

@app.route('/generate_contract', methods=['POST'])
def generate_contract():
    try:
        # Load template
        doc = DocxTemplate(TEMPLATE_PATH)

        # Get form data from frontend
        data = request.get_json()

        # Prepare context with fallback empty strings
        context = {
            'name': data.get('name', ''),
            'passport_number': data.get('passport_number', ''),
            'pp_expiry_date': data.get('pp_expiry_date', ''),
            'dob': data.get('dob', ''),
            'address': data.get('address', ''),
            'work_start_date': data.get('work_start_date', ''),
            'work_end_date': data.get('work_end_date', ''),
            'country': data.get('country', ''),
            'cont_fisical': data.get('cont_fisical', ''),
            'niss_num': data.get('niss_num', ''),
            'worded_date': data.get('worded_date', ''),
        }

        # Render document with data
        doc.render(context)

        # Save result
        output_path = 'generated_contract.docx'
        doc.save(output_path)

        # Return file for download
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run()

