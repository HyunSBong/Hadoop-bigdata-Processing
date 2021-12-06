import urllib.request
import json
import pandas as pd
import signal

# 시간초과 방지
class TimeOutException(Exception): 
    pass

def alarm_handler(signum, frame): 
    print("시간초과") 
    raise TimeOutException()

# 네이버 검색 API
def naverAPI(encText, start, display):
  url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&start=" +  start + "&display=" + display
  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id", "s5iCF6EO8OmXidvMpaJ6")
  request.add_header("X-Naver-Client-Secret", "IrC3CiuFUt")
  try:
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
      data = response.read().decode('utf-8')
      return json.loads(data)
    else:
      print("Error Code:" + rescode)
  except:
    return

df = pd.read_csv("여행지키워드.csv")
df = df.drop_duplicates()
l = df.values.tolist()
count = 0
for i in l:
  print("남은 개수 : " + str(len(l) - count))
  count += 1
  signal.signal(signal.SIGALRM, alarm_handler) 
  signal.alarm(6) # 6초이상 걸린다면 오류 이므로 다음 loop로 넘긴다.
  try: 
    jsonArr = []
    encText = i[1].strip()
    start = "1"
    display = "100"
    
    # api 호출
    data = naverAPI(encText, start, display)
    while (data != None):
      # 배열에 json 데이터 추가
      for j in data:
        jsonArr.append({'title' : j['title'], 'description': j['description'], 'link': j['link']})
      # 시작지점 + display 다음부터 api 재호출
      next = int(data["start"]) + int(data["display"])
      # next가 1000이면 api 제한 회수보다 크므로 종료
      if (next >= 1000):
        break
      else:
        data = naverAPI(encText, next, display)
    
    with open("naver_data/" + encText + "_naver_blog.json", 'w', encoding='utf8-sig') as outfile:
      outfile.write(json.dumps(jsonArr,indent=4, sort_keys=True, ensure_ascii=False))
  except TimeOutException as e: 
    print(e)
    pass
