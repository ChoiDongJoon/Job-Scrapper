"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, redirect
from sof import get_jobs as sof_get_jobs
from wwr import get_jobs as wwr_get_jobs
#from remoteok import get_jobs as ok_get_jobs

app = Flask("Scrapper")
db = {}



@app.route("/") #home
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word) #db에 찾는 word가 있는지 확인
    if existingJobs: #있으면
      jobs = existingJobs
    else: #없으면
      sof_jobs = sof_get_jobs(word)
      wwr_jobs = wwr_get_jobs(word)
      #ok_jobs = ok_get_jobs(word)
      jobs = sof_jobs + wwr_jobs #+ ok_jobs
  else:
    return redirect("/")
  return render_template("report.html",     resultsNumber=len(jobs), 
searchingBy = word,
jobs = jobs) #report.html로 검색어 넘겨주기

app.run(host = "0.0.0.0")

#분명 2월 26일 토요일에는 됐던 remoteok 스크랩이 어떤 이유에선지 갑자기 안되네요..