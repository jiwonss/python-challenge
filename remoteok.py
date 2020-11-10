import requests
from bs4 import BeautifulSoup


def extract_job(html):
    if 'd' in html.find("time").get_text():
        title = html.find("h2").get_text()
        company = html.find("h3").get_text()
        link = html.find("a", {"class": "preventLink"})['href']
        return {'title': title, 'company': company, 'link': f"https://remoteok.io{link}"}


def extract_jobs(term):
    jobs = []
    url = f"https://remoteok.io/remote-{term}-jobs"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find("div", {"class": "page"}).find(
        "div", {"class": "container"}).find("table")
    results = table.find_all("tr", {"class": "job"})
    for result in results:
        job = extract_job(result)
        if job is not None:
            jobs.append(job)
    return jobs
