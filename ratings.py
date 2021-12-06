import pandas as pd

def main():
  old_nameArr = []
  old_numArr = []
  hospital_nameArr = []
  hospital_moveArr = []
  hospital_bedArr = []
  old_df = pd.read_csv("전국지자체별_고령인구비율.csv")
  for i in old_df.itertuples():
    name = str(i[1]) # 지자체명
    oldNum = float(i[2]) # 고령인구 비율
    old_nameArr.append(name)
    old_numArr.append(oldNum)
  hospital_df = pd.read_csv("전국지자체별_유동인구_병원_병상데이터.csv")
  for i in hospital_df.itertuples():
    name = str(i[1]) # 지자체명
    moveNum = str(i[2]) # 유동인구 데이터
    bedNum = str(i[4]) # 병상 수
    # 데이터 정제
    if ("만명" in moveNum):
      moveNum = moveNum[:-2] + "0000"
      if ("," in moveNum):
        moveNum = moveNum.replace(',', '')
    if ("명" in moveNum):
      moveNum = moveNum[:-1]
      if ("," in moveNum):
        moveNum = moveNum.replace(',', '')  
    if ("개" in bedNum):
      bedNum = bedNum[:-1]
      if ("," in bedNum):
        bedNum = bedNum.replace(',', '') 
    hospital_nameArr.append(name)
    hospital_moveArr.append(moveNum)
    hospital_bedArr.append(bedNum)

  hospital_nameArr2 = []
  hospital_moveArr2 = []
  hospital_bedArr2 = []
  for i in range(len(hospital_nameArr)):
    if (hospital_nameArr[i] in old_nameArr):
      hospital_nameArr2.append(hospital_nameArr[i])
      hospital_bedArr2.append(hospital_bedArr[i])
      hospital_moveArr2.append(hospital_moveArr[i])

  resultArr = []
  for i in range(len(hospital_nameArr2)):
    # (유동인구 / 병상수) * 고령인구 비율
    try:
      data = (int(hospital_moveArr2[i]) / int(hospital_bedArr2[i])) * int(old_numArr[i])
      resultArr.append(data)
    except:
        resultArr.append(0)

  df = pd.DataFrame()
  df["지자체명"] = hospital_nameArr2
  df["통계치"] = resultArr
  # csv 저장
  df.to_csv("전국지자체별_통계데이터.csv", encoding='utf-8-sig', header=True, index=True)

if __name__=='__main__':
  main()
  