import requests
from bs4 import BeautifulSoup
#html에서 데이터를 추출하는데에는 beautifulsoup 사용
#find는 찾은 첫번째 값. find_all은 전부


#step 1: 페이지 가져오기 step 2: request 만들기 step 3: job 추출하기

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class" : "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True) # strip=True -> 공백 없애기 
    return int(last_page)

def extract_job(html):
    title = html.find("div", {"class":"flex--item fl1"}).find("h2").find("a")["title"]
    company, location = html.find("h3",{"class":"fc-black-700 fs-body1 mb4"}).find_all("span",
    recursive = False) #span안의 span을 가져오는 것을 방지 #리스트에 요소가 두가지가 있는 것을 아니까 company, location으로 가능 
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {'title':title, 'company':company, 'location':location, 'link':f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{url}&pg={page + 1}") # page 1부터 시작 0은 previos 버튼 
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page,url)
    return jobs