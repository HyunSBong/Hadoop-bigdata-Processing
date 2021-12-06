
import re
import pandas as pd
from konlpy.tag import Okt
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import json

class KnuSL():

	def data_list(wordname):	
		with open('KnuSentiLex-master/KnuSentiLex/data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
			data = json.load(f)
		result = ['None','None']	
		for i in range(0, len(data)):
			if data[i]['word'] == wordname:
				result.pop()
				result.pop()
				result.append(data[i]['word_root'])
				result.append(data[i]['polarity'])	
		
		r_word = result[0]
		s_word = result[1]	
		
		return s_word

def knuSL(word):
	
	ksl = KnuSL

	
	wordname = word.strip(" ")	
	return ksl.data_list(wordname)

def sensilbility(arr):
  data = arr
  result = []
  grade = 0 # 감정 점수
  for content in arr:
    for word in content:
      # 감성분석 (KNU 한국어 감성 사전)
      data = knuSL(word)
      if (data != None and data != "None"):
        grade += int(data)
  return grade

# 불용어제거
def stopword_cleaner(df):
  arr = [] # 불용어가 제거된 본문 데이터 배열
  result_df = df
  for i in result_df.itertuples():
    rowData = str(i[4])
    # 1차 정제
    rowData = re.sub(pattern='([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', repl="", string= rowData)
    rowData = re.sub(pattern='<[^>]*>', repl="", string= rowData)
    rowData = re.sub(pattern='[^\w\s]', repl="", string= rowData)
    rowData = re.sub(pattern='[0-9]+', repl="", string= rowData)

    # 2차 정제
    tokens = word_tokenize(rowData)
    stopWords_df = pd.read_csv("불용어리스트.csv")
    stopWords = stopWords_df.values.tolist()
    cleaning = [word for word in tokens if not word in stopWords]
    joined = ",".join(cleaning)

    # 3차 정제
    # KoNLPy 형태소 분석기
    okt = Okt()
    for i in okt.pos(joined, stem = True):
      if (i[1] in ['Adjective']): # 형용사인경우
        arr.append(i[0])
  return arr

def main():
  # 지역명 추출
  names = []
  base_df = pd.read_csv("전국지자체별_유동인구_병원_병상데이터.csv")
  for i in base_df.itertuples():
    rowData = str(i[1]).split("(") # 서귀포시(제주특별자치도) 형식이므로 (로 분리
    if (len(rowData) == 1):
      continue
    localgovName = rowData[0].strip() # 기초자치단체명
    govName = rowData[1][:-1] # 전체 광역자치단체명

    if ("광역시" in rowData[1] or "특별" in rowData[1] or len(rowData[1]) == 4):
      govName2 = rowData[1][0:2]
      names.append(localgovName + " " + govName + " " + govName2)
    else:
      govName2 = rowData[1][0] + rowData[1][2]
      names.append(localgovName + " " + govName + " " + govName2)

  base_df = pd.read_csv("여행지키워드.csv")
  l = base_df.values.tolist()

  for i in l:
    try:
      fileName = i[1].strip() + "_블로그본문데이터.csv"
      fileName_split = i[1].split(" ")
      if ("여행지" in fileName_split[1]):
        for govName in names:
          if (fileName_split[0] in govName):
            govName = govName.split(" ")
            namesArr.append(govName[0].strip() + "(" + govName[1].strip() + ")")
            break
      else:
        for govName in names:
          govName = govName.split(" ")
          if (fileName_split[0] in govName and fileName_split[1] in govName):
            namesArr.append(govName[0].strip() + "(" + govName[1].strip() + ")")
            break
    except:
      continue
    df = pd.DataFrame()
    try:
      df = pd.read_csv("naver_data_content/" + fileName, header=0, lineterminator='\n', index_col=0)
    # 파일이 없는 경우 다음 loof로 건너뜀
    except:
      print("파일 없음")
      continue

    # 불용어 제거
    cleanArr = []
    cleanArr = stopword_cleaner(df)

   # 감성분석 (KNU 한국어 감성 사전)
    sensilbilityGrade = sensilbility(cleanArr)
    sensilbilityGradeArr.append(sensilbilityGrade)
  result_df = pd.DataFrame()
  result_df["지자체명"] = namesArr
  result_df["감성지수"] = sensilbilityGradeArr
  # csv 저장
  try:
    result_df.to_csv("naver_data_content/감성지수 데이터.csv", encoding='utf-8-sig', header=True)
  except:
    pass

namesArr = []
sensilbilityGradeArr = []

if __name__=='__main__':
  main()

  