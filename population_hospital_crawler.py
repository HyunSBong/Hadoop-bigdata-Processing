from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from selenium import webdriver

# 한국 데이터 산업 진흥원 
# http://datakorea.datastore.or.kr/profile/geo/01000KR/#%EC%9C%A0%EB%8F%99%EC%9D%B8%EA%B5%AC

def get_total_population(gov):
  base_url = "http://datakorea.datastore.or.kr/profile/geo/"
  url = base_url + gov

  # 광역자치단체 유동인구 추출
  driver.get(url)
  time.sleep(3)
  # 유동인구 페이지로 이동
  click_target = driver.find_element_by_xpath('//*[@id="splash"]/div[2]/div[3]/a[6]')
  click_target.click()
  time.sleep(5)

  url = driver.current_url

  linkArr = [] # 기초자치단체별 링크만 잠깐 담을 변수
  # 현재 광역자치단체명 추출
  soup = bs(driver.page_source, 'html.parser')
  govName = soup.select_one("#splash > div.content > div.splash-titles > h1 > span:nth-of-type(1)")
  govNameArr.append(govName.get_text())
  # 유동인구 추출
  govNum = soup.select_one("body > section.유동인구.profile-section > article:nth-of-type(1) > div > aside > div.topic-stats > div:nth-of-type(1) > div.stat-value > span > span")
  numArr.append(govNum.get_text())

  # 각 기초자치단체별 링크추출
  base_url = "http://datakorea.datastore.or.kr"
  big_local_gov = soup.find("div", "breadcrumb").find_all("a")
  for link in big_local_gov:
    # 전국 제외
    if (link.get_text() == "전국"):
      continue
    linkArr.append(base_url + link.attrs["href"])

  # 기초자치단체별 명칭, 유동인구 추출
  for link in linkArr:
    driver.get(link)
    time.sleep(3)
    # 유동인구 페이지로 이동
    click_target = driver.find_element_by_xpath('//*[@id="splash"]/div[2]/div[3]/a[6]')
    click_target.click()
    time.sleep(5)
    # 기초자치단체의 명칭, 유동인구 추출
    soup = bs(driver.page_source, 'html.parser')
    govName = soup.select_one("#splash > div.content > div.splash-titles > h1 > span:nth-of-type(1)")
    govNum = soup.select_one("body > section.유동인구.profile-section > article:nth-of-type(1) > div > aside > div.topic-stats > div:nth-of-type(1) > div.stat-value > span > span")
     # 병원 및 병상 수 추출
    hospital = soup.select_one("body > section.건강및안전.profile-section > article:nth-child(3) > div > aside > div.topic-stats > div:nth-child(1) > div.stat-value > span > span")
    bed = soup.select_one("body > section.건강및안전.profile-section > article:nth-child(3) > div > aside > div.topic-stats > div:nth-child(2) > div.stat-value > span > span")
    
    govNameArr.append(govName.get_text())
    try:
      numArr.append(govNum.get_text())
    except:
      numArr.append("nan")
    try:
      hospitalArr.append(hospital.get_text())
    except:
      hospitalArr.append("nan")
    try:
      bedArr.append(bed.get_text())
    except:
      bedArr.append("nan")
    
if __name__=='__main__':
  path = "/Users/hyunsubong/OneDrive - 명지대학교/Univ/2021-2/빅데이터 프로그래밍/project/chromedriver_m1"
  driver = webdriver.Chrome(path)

  govList = ["seoul", "gyeonggi-do", "gangwon-do", "chungcheongnam-do", "chungcheongbuk-do", "jeollanam-do", "jeollabuk-do", "gyeongsangnam-do", "gyeongsangbuk-do", "jeju"]
  govNameArr = [] # 자치단체명을 담을 전역변수
  numArr = [] # 유동인구수를 담을 전역변수
  hospitalArr = [] # 병원 수를 담을 전역변수
  bedArr = [] # 병상 수를 담을 전역변수

  # 광역자치단체별 유동인구 수집
  for i in govList:
    get_total_population(i)

  print(len(govNameArr))
  print(len(hospitalArr))
  print(len(bedArr))
  # csv 저장
  df = pd.DataFrame()
  df["지자체명"] = govNameArr
  df["전체유동인구"] = numArr
  df["병원 수"] = hospitalArr
  df["병상 수"] = bedArr
  df.to_csv("전국지자체별_유동인구_병원_병상데이터.csv", encoding='utf-8-sig', header=True)

