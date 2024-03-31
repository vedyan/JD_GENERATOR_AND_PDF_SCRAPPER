import google.generativeai as genai
from config import GEMINI_API_KEY


def post_process_text(text):
    cleaned_text = text.replace("**", "")
    return cleaned_text


def generate_job_description(job_title, location, mandatory_skills, overall_experience, work_type, mode_of_work
                             , education_requirement, ctc):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    jd = (f"Job Description for {job_title} at {location} if any\n Skills: {', '.join(mandatory_skills)}\n"
          f"Experience: {overall_experience} years\n"
          f"Work Type: {work_type}\n Mode of Work: {mode_of_work}"
          f"The JD should be in the following format : \n"
          f"Job title : {job_title}\n"
          f"Summary : it should include the brief about the {job_title} the location of work {location} if and the "
          f"type of work {work_type} and the mode of work {mode_of_work}\n"
          f"Responsibilities/Duties: \n"
          f"{education_requirement} and {overall_experience} and {mandatory_skills} and any other additional skills "
          f"under Qualifications and skills: \n"
          f"Mandatory Skills: {mandatory_skills}\n"
          f"Education Requirements: {education_requirement}\n"
          f"Experience: {overall_experience}\n"
          f"CTC Range:{ctc}\n"
          f"Equal Opportunity Employer:\nWe are proud to be an Equal Opportunity Employer with a global culture that "
          f"embraces diversity. We are committed to providing an environment free of unfair discrimination and "
          f"harassment. We do not discriminate based on age, race, colour, sex, religion, national origin, "
          f"disability, pregnancy, marital status, sexual orientation, gender reassignment, veteran status, "
          f"or other protected category.\n\n the end of the job description should always include the above Equal "
          f"Opportunity Employer paragraph"
          )
    response = model.generate_content(jd)
    return post_process_text(response.text)
