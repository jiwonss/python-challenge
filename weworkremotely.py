import requests
from bs4 import BeautifulSoup


def extract_job(html):
    title = html.find("span", {"class": "title"}).get_text()
    link = html.find("a")['href']
    company = html.find("span", {"class": "company"}).get_text()
    return {'title': title, 'compoany': company, 'link': f"https://weworkremotely.com{link}"}


def extract_jobs(term):
    jobs = []
    url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("div", {"class": "content"}).find(
        "section", {"id": "category-2"}).find_all("li", {"class": "feature"})
    for result in results:
        job = extract_job(result)
        if job is not None:
            jobs.append(job)
    return jobs
