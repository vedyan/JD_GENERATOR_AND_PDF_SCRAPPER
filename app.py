from flask import Flask, request, jsonify, render_template
import requests
import fitz  # PyMuPDF
import PyPDF2
import gemini

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


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

        if job_title and location and overall_experience and mandatory_skills and work_type and mode_of_work and education_requirement and ctc:
            jd_text = gemini.generate_job_description(job_title, location, mandatory_skills, relative_experience, overall_experience, work_type, mode_of_work, education_requirement, ctc)
            return jsonify({'job_description': jd_text}), 200
        else:
            return jsonify({'error': 'Missing required fields.'}), 400
    else:
        return jsonify({'error': 'Invalid request format.'}), 400


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
