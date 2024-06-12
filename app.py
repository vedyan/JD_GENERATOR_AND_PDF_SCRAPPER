from flask import Flask, request, jsonify, render_template
import requests
import fitz  # PyMuPDF
import PyPDF2
import gemini
from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "https://app.rework.club/"}})

CORS(app, resources={r"/*": {"origins": "https://app.rework.club"}})

@app.route('/job_description', methods=['POST'])
def generate_job_description():
    if request.json:
        data = request.json
        job_title = data.get('job_title')
        location = data.get('location')
        mandatory_skills = data.get('mandatory_skills', [])
        relative_experience = data.get('relative_experience')
        overall_experience = data.get('overall_experience')
        work_type = data.get('work_type')
        mode_of_work = data.get('mode_of_work')
        education_requirement = data.get('education_requirement')
        ctc = data.get('ctc')

        missing_fields = []
        if not job_title:
            missing_fields.append('job_title')
        if not location:
            missing_fields.append('location')
        if not overall_experience:
            missing_fields.append('overall_experience')
        if not mandatory_skills:
            missing_fields.append('mandatory_skills')
        if not work_type:
            missing_fields.append('work_type')
        if not mode_of_work:
            missing_fields.append('mode_of_work')
        if not education_requirement:
            missing_fields.append('education_requirement')
        if not ctc:
            missing_fields.append('ctc')

        if missing_fields:
            return jsonify({'error': 'Missing required fields.', 'missing_fields': missing_fields}), 400
        else:
            jd_text = gemini.generate_job_description(job_title, location, mandatory_skills, relative_experience, overall_experience, work_type, mode_of_work, education_requirement, ctc)
            return jsonify({'job_description': jd_text}), 200
    else:
        return jsonify({'error': 'Invalid request format.'}), 400
# @app.route('/job_description', methods=['POST'])
# def generate_job_description():
#     if request.json:
#         data = request.json
#         job_title = data.get('job_title')
#         location = data.get('location')
#         mandatory_skills = data.get('mandatory_skills', [])
#         relative_experience = data.get('relative_experience')
#         overall_experience = data.get('overall_experience')
#         work_type = data.get('work_type')
#         mode_of_work = data.get('mode_of_work')
#         education_requirement = data.get('education_requirement')
#         ctc = data.get('ctc')

#         if job_title and location and overall_experience and mandatory_skills and work_type and mode_of_work and education_requirement and ctc:
#             jd_text = gemini.generate_job_description(job_title, location, mandatory_skills, relative_experience, overall_experience, work_type, mode_of_work, education_requirement, ctc)
#             return jsonify({'job_description': jd_text}), 200
#         else:
#             return jsonify({'error': 'Missing required fields.'}), 400
#     else:
#         return jsonify({'error': 'Invalid request format.'}), 400


@app.route('/pdf_job_description', methods=['POST'])
def generate_job_description_from_pdf():
    if 'pdf_file' in request.files:
        pdf_file = request.files['pdf_file']
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = ''
        for page_num in range(len(pdf_reader.pages)):
            pdf_text += pdf_reader.pages[page_num].extract_text()
        reformated_text = gemini.reformat_job_description(pdf_text)
        return jsonify({'job_description': reformated_text}), 200
    return jsonify({'error': 'PDF file not provided.'}), 400


@app.route('/pdf_job_description_s3', methods=['POST'])
def generate_job_description_from_url():
    pdf_url = request.json.get("pdf_url")

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_data = response.content

        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        reformated_text = gemini.reformat_job_description(text)
        return jsonify({'job_description': reformated_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
