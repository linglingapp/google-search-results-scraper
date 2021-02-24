from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs
from save import save_to_file
import os

app = Flask("SuperScraper")

db = {}

@app.route("/")
def home():
  return render_template("main.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html",
    term=word,
    resultNumber=len(jobs),
    results=jobs
  )
  
@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("results.csv")
  except:
    return redirect("/")

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)