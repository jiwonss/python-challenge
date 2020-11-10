from flask import Flask, render_template, request, send_file, redirect
from stackoverflow import get_jobs as so_get_jobs
from weworkremotely import extract_jobs as we_get_jobs
from remoteok import extract_jobs as re_get_jobs
from exporter import save_to_file

db = {}
app = Flask("RemoteJobs")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    term = request.args.get('term')
    term = term.lower()
    existingJobs = db.get(term)
    if existingJobs:
        jobs = existingJobs
    else:
        jobs = so_get_jobs(term) + we_get_jobs(term) + re_get_jobs(term)
        db[term] = jobs
    save_to_file(term, jobs)
    return render_template("search.html", jobs=jobs, jobs_cnt=len(jobs), term=term)


@app.route("/export")
def export():
    try:
        term = request.args.get('term')
        term = term.lower()
        jobs = db.get(term)
        if not jobs:
            raise Exception()
        file_name = f"{term}.csv"
        save_to_file(term, jobs)
        return send_file(file_name, as_attachment=True, attachment_filename=file_name)
    except:
        return redirect("/")


app.run(host="0.0.0.0")
