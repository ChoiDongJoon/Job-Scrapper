import requests, os
from bs4 import BeautifulSoup

def extract_job(box):
  title = box.find("span", {"class":"title"}) 
  title = title.get_text(strip=True)
      
  company = box.find("span", {"class":"company"})
  company = company.get_text(strip=True)
  
  region = box.find("span",{"class": "region"})
  if region is not None:
    region = region.get_text(strip=True)
  else:
    region = "None"
  
  link = box.find_next("a")["href"]
  link = "https://weworkremotely.com/" + link

  return {'title': title, 'company' : company, 'location' : region, 'link' : link}

def extract_jobs(url):
  jobs = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  container = soup.find("div", {"class":"jobs-container"})
  sections = container.find_all("section", {"class":"jobs"})
  for section in sections:
    boxes = section.find_all("li", {"class" : "feature"})
    for box in boxes:
      job = extract_job(box)
      jobs.append(job)
  
  all = container.find("li",{"class":"view-all"})
  more_link = all.find("a")["href"]
  more_link = "https://weworkremotely.com/" + more_link
  m_result = requests.get(more_link)
  m_soup = BeautifulSoup(m_result.text, "html.parser")
  m_container = m_soup.find("div",{"class":"jobs-container"})
  m_section = m_container.find("section",{"class":"jobs"})
  m_boxes = m_section.find_all("li",{"class":"feature"})
  for box in m_boxes[:-1]:
    m_job = extract_job(box)
    jobs.append(m_job)
  return jobs
  
def get_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(url)
  return jobs

