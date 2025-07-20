import fitz   #read pdf files and get content
import docx
import os
import re  #pattern match
import openai



#client=openai.OpenAI(api_key="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")



#def extract_text_pdf(pdf_path):  #func get text from pdf ,join in 1 string and return
 #   doc=fitz.open(pdf_path)
  #  text=""
   # for page in doc:
    #    text+=page.get_text()
    #return text
def extract_text_pdf(pdf_path):
    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text










def extract_fields(text):
    data={}    #hold info to store mail,no etc.

    mail_match=re.search(r'\S+@\S+',text)
    data['mail']=mail_match.group() if mail_match else None

    phone_match=re.search(r'(\+91[\s\-]?)?\(?\d{3,5}\)?[\s\-]?\d{5}',text)    #\d{10} means 10 digits in a row
    data['phone']=phone_match.group() if phone_match else None

    skill_keywords=['python','html','css','javascript','web development','video editing','marketing','java','c','c++']
    skills_found=[]
    for skill in skill_keywords:
        pattern=r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern,text.lower()):
            skills_found.append(skill)
    data['skills']=skills_found

    github=re.search(r'https:\/\/github\.com\/\S+',text)
    linkedin=re.search(r'https:\/\/www\.linkedin\.com\/\S+',text)    #\S+ keep matching until space
    data['github']=github.group() if github else None
    data['linkedin']=linkedin.group() if linkedin else None
    return data



def extract_skills(text, skill_list):
    print("extract_skills received:", type(text), text[:100])

    # ✅ Normalize 'text' input
    if isinstance(text, list):
        text = " ".join(str(item) if isinstance(item, str) else str(item.get("text", "")) if isinstance(item, dict) else "" for item in text)
    elif isinstance(text, dict):
        text = " ".join(str(value) for value in text.values() if isinstance(value, str))

    found = set()
    for skill in skill_list:
        if skill.lower() in text.lower():
            found.add(skill)
    return found

    


#def extract_text_docx(docx_path):
 #   doc=docx.Document(docx_path)
   # text="\n".join([p.text for p in doc.paragraphs])
  #  return text

def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_pdf(file_path)
    else:
        raise ValueError("Unsupported format")
    
def match_resume_to_job(resume_text,job_text,skill_list):
    resume_skills=extract_skills(resume_text,skill_list)
    job_skills=extract_skills(job_text,skill_list)
    if not job_skills:
        return 0,[],resume_skills,job_skills
    matched=resume_skills.intersection(job_skills)
    match_percent=(len(matched)/len(job_skills))*100

    return round(match_percent,2),list(matched),resume_skills,job_skills
#def gpt_feedback(resume_text,role):
#      prompt=f"Here is a resume: \n\n{resume_text}\n\nSuggest how it can be improved to get better job matches and what new skills to learn.Be specific and helpful."
#      try:
 #        response=client.chat.completions.create(
 #           model="gpt-3.5-turbo",
  #          messages=[{"role":"user","content":prompt}
                     
       #               ]
      #                 )
 #        return response.choices[0].message.content.strip()
  #    except Exception as e:
  #       return f"gpt error:{e}"





#pdf_path=r"C:\Users\yadav\Downloads\ANSHIKA Y .pdf"
#resume_text=extract_text_pdf(pdf_path)
#parsed_data=extract_fields(resume_text)
#print(parsed_data)