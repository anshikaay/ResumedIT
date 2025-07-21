import requests
import os
from dotenv import load_dotenv

from resume import extract_text_pdf,match_resume_to_job,extract_fields,extract_skills
from flask import Flask,request,jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app,origins=["http://127.0.0.1:5500"])

#pdf_path=r"C:\Users\yadav\Downloads\ANSHIKA Y .pdf"





skills=['python','html','css','javascript','web development','video editing','marketing','java','c','c++']

def fetch_jobs(query="developer jobs in india",page=1):
    url="https://jsearch.p.rapidapi.com/search"
    querystring={"query":query,
                 "page":str(page),
                 "num_pages":"1",
                 "country":"india",
                 "date_posted":"all"
                 }
    headers={
        "x-rapidapi-host":"jsearch.p.rapidapi.com",
        "x-rapidapi-key":os.getenv("x-rapidapi-key")
    }
    response=requests.get(url,headers=headers,params=querystring)
    if response.status_code==200:
        jobs=response.json().get("data",[])
        return jobs
    else:
        print("Error:",response.status_code,response.text)
        return []
@app.route('/match',methods=['POST'])
def match():  
    
    resume_file=request.files["resume"]
    role=request.form.get("role")
    if not resume_file or not role:
          return jsonify({"error":"Missing resume or role"}),400
    
    resume_text=extract_text_pdf(resume_file)
    parsed=extract_fields(resume_text)
    resume_skills=set(parsed['skills'])

    jobs=fetch_jobs(query=role)
   


    
    job_results = fetch_jobs(role)
    matched_jobs = match_resume_to_job(resume_text, job_results, skills)
   # feedback = gpt_feedback(resume_text, role)




    results=[]
    for job in job_results:
       job_desc=job.get("job_description","")
       score,matched,_,_=match_resume_to_job(resume_text,job_desc,skills)
       results.append({
        "title":job.get("job_title"),
        "company":job.get("employer_name"),
        "score":score,
        "matched_skills":list(matched),
        "link":job.get("job_apply_link","#")
    })
    sorted_jobs=sorted(results,key=lambda x: x["score"],reverse=True)[:5]
    
    
    return jsonify({
          "jobs":sorted_jobs
      #    ,"feedback":feedback
    })

@app.route("/",methods=["GET"])
def home():
    return "ResumedIT backend is live. "
if __name__=="__main__":
      app.run(port=5000)