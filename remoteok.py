import requests, os
from bs4 import BeautifulSoup

def extract_job(company):  
  title = company.find("h2")
  title = title.get_text(strip=True)
  
  company_name = company.find("h3", {"itemprop": "name"})
  company_name = company_name.get_text(strip=True)
  
  location = company.find("div", {"class" : "location"})
  location = location.get_text(strip=True)

  link = company.find("a")["href"]
  link = "https://remoteok.com/" + link

  return {'title': title, 'company' : company_name, 'location' : location, 'link' : link}
  
def extract_jobs(soup):
  
  board = soup.find("table",{"id":"jobsboard"})
  companys = board.find_all("td",{"class":"company position company_and_position"})
  jobs = []
  for company in companys[1:]:
    job = extract_job(company)
    jobs.append(job)
  return jobs

def get_jobs(word):
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
  url = f"https://remoteok.com/remote-dev+{word}-jobs"
  result = requests.get(url, headers = headers)
  soup = BeautifulSoup(result.text, "html.parser")
  jobs = extract_jobs(soup)
  return jobs
