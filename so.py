import requests, time
from bs4 import BeautifulSoup

def get_last_page(url):
  # Goolgeのようなサイトは「headers」を設定しないと「parser」がうまくできない。cf. inspector, DOM
  headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
  result = requests.get(url, headers=headers)
  if result.status_code == 200:
    print("短時間で多くのリクエストを要請した場合は「429」が帰ってきます（「Internal Server Error」と表示される）。", result)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("table", {"class":"AaVjTc"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    print("表示件数100件で検索した結果，" + last_page + "ページがありました。")
    time.sleep(5)
  else:
    print("短時間で多くのリクエストを要請したので，Googleに怒られています。解除まで数時間かかります。")
  return int(last_page)

def extract_job(html):
  title=html.find("h3",{"class":"LC20lb DKV0Md"}).find("span").get_text(strip=True)
  snippet = html.find("div", {"class":"IsZvec"}).find("span").get_text(strip=True)
  # snippet = snippet.get_text(strip=True)
  job_id = html.find("div", {"class":"yuRUbf"}).find("a")["href"]
  return {'TITLE': title, 'SNIPPET': snippet, 'apply_link': job_id}

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    result = requests.get(f"{url}&start={page}00", headers=headers)
    print(f"{page+1}ページ目の検索結果を収集します。")
    time.sleep(5)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"tF2Cxc"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs(word):
  url = f"https://www.google.com/search?q={word}&num=100"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs