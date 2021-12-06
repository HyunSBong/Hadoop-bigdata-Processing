import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_gov_name():
  arr = []
  url = "https://ko.wikipedia.org/wiki/대한민국의_기초자치단체_목록"
  req = requests.get(url)
  soup = bs(req.text, 'html.parser')

  for i in range(2,228):
    print(i)
    tag = soup.select_one('#mw-content-text > div.mw-parser-output > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(1) > a').get_text()
    arr.append(tag + " 여행지") # 중구 여행지
    if (len(tag) != 2):
        arr.append(tag[:-1] + " 여행지") # 수원 여행지

    tag_gov = soup.select_one('#mw-content-text > div.mw-parser-output > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2)').get_text()

    if ("광역시" in tag_gov or "특별시" in tag_gov):
      arr.append(tag_gov[:-3] + " 여행지") # 서울특별시 -> 서울 여행지
      arr.append(tag_gov[:-3] + " " + tag + " 여행지") # 서울 강남구 여행지
      if (len(tag) != 2):
        arr.append(tag_gov[:-3] + " " + tag[:-1] + " 여행지") # 서울 + 강남 여행지
    else:
      if(len(tag_gov) == 4):
        tag_gov = tag_gov[0] + tag_gov[2] # 충청남도 -> 충남
        arr.append(tag_gov + " 여행지") # 충남 여행지
        arr.append(tag_gov + " " + tag + " 여행지") # 충남 천안시 여행지
        if (len(tag) != 2):
          arr.append(tag_gov + " " + tag[:-1] + " 여행지") # 충남 천안 여행지
    
  
  return arr

if __name__=='__main__':
  resultArr = []
  resultArr = get_gov_name()
  resultArr.append("세종 여행지")
  df = pd.DataFrame()
  df["키워드"] = resultArr
  df.to_csv("기초자치단체별_여행지키워드.csv", encoding='utf-8-sig', header=True)
