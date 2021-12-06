import multiprocessing
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

# 네이버블로그 본문
def get_blog_content(url, text_arr):

  # 주소가 daum일 경우
  if ("blog.daum.net" in url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    text = soup.find("div", "tt_article_useless_p_margin contents_style")
    if (text == None):
      return
    text_arr.append(text.get_text())
    return
  
  # 즈소가 naver인 경우
  try:
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "lxml") 
    url = "https://blog.naver.com/" + soup.iframe["src"]

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "lxml") 

    if soup.find("div", id = "postViewArea"):
      text = soup.find("div", id = "postViewArea").get_text()
      text = text.replace("\n","")
      text_arr.append(text)
      return

    elif soup.find("div", id = "postViewArea"):
      text = soup.find("div", id = "postViewArea").get_text()
      text = text.replace("\n","") 
      text_arr.append(text)
      return
    else:
      text = soup.find('div', 'se-component se-text se-l-default')
      text_arr.append(text)
      return
  except:
    return

# 기초 정보 수집 (링크)
def pre_processing(lists, k):
  l = lists
  j = 0 # 전체 count용
  for gov in l[k:]:
    fileName = gov[1].strip() + "_naver_blog.json"
    # 지역명으로 해당 블로그 json 파싱파일 열기
    try:
      with open("naver_data/" + fileName, encoding='UTF-8-sig') as f:
        jsonData = json.load(f)
    except:
      print("파일 없음 pass")
      return False

    i = 0
    c = len(jsonData)
    while (c >= 0):
      try:
        list_to_json = json.dumps(jsonData[i], ensure_ascii=False) # json 내 첫번째 데이터
        json_to_dict = json.loads(list_to_json)
        json_link = json_to_dict["link"]
        json_description = json_to_dict["description"]
        govNameArr.append(gov[1].strip())
        linkArr.append(json_link)
        descriptionArr.append(json_description)
      except:
        pass
      c -= 1
      i += 1
      print(gov[1] + "의 전체" + str(len(jsonData)) + "개 중" + str(len(jsonData)-c) + "개 수행 ==> " + str(c) + "개 남음") # 진행 상황 체크
    j += 1
    if (j == 1): # k 인덱스에 해당하는 파일만 처리하도록
      break

status = True

if __name__=='__main__':
  # 본문 파싱을 위한 링크 등 정보 수집
  df = pd.read_csv("여행지키워드.csv")
  l = df.values.tolist()

  for k in range (0, len(l)):
    print("남은 개수 ==> " + str(len(l) - k)) # 남은 작업 확인용
    status = True
    df_post = pd.DataFrame() # 본문이 포함될 최종 데이터 프레임

    # 데이터프레임의 각 열에 해당하는 행에 들어갈 정보를 담을 전역 변수
    govNameArr = [] # 지자체명
    linkArr = [] # 블로그 링크
    descriptionArr = [] # 본문 요약
    textArr = [] # 본문

    status = pre_processing(l, k)
    if (status == False): # 실패시 넘기기
      continue

    # 데이터프레임에 데이터 추가
    df_post["지자체"] = govNameArr
    df_post["블로그링크"] = linkArr
    df_post["요약"] = descriptionArr
    df_post["본문"] = ""

    # 병렬처리
    m = multiprocessing.Manager()
    textArr = m.list()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.starmap(get_blog_content, [(url, textArr) for url in linkArr])
    pool.close()
    pool.join()

    # 본문 데이터 추가
    for i in range(len(textArr)):
      df_post.iloc[i, 3] = textArr[i]

    # csv 저장
    try:
      df_post.to_csv("naver_data_content/" + govNameArr[k] + "_블로그본문데이터.csv", encoding='utf-8-sig', header=True)
    except:
      pass