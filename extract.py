import requests
import os
from dotenv import load_dotenv

from resume import extract_text_pdf,match_resume_to_job,extract_fields,extract_skills
from flask import Flask,request,jsonify
from flask_cors import CORS

from flask import send_from_directory



app=Flask(__name__)
CORS(app)







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
        "x-rapidapi-key":"4096652826mshc31af4443a70939p18657ejsndabcc32f33f8"
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
    print("hello")
    print("request method",request.method)
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

@app.route("/")
def serve_html():
    return send_from_directory('.','resume.html',as_attachment=False)

@app.route("/resume.css")
def serve_css():
    return send_from_directory('.','resume.css',as_attachment=False)

@app.errorhandler(404)
def not_found(e):

    return send_from_directory('.','resume.html')


if __name__=="__main__":
      app.run(port=5000)