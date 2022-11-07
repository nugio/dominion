
import pandas as pd 
import random
data= pd.read_csv('pytest.csv' , encoding="shift-jis")
data.head()

class Card:
  def __init__(self, index,exset,name, cost,action2,attack):
    self.index =index
    self.exset = exset
    self.name = name
    self.cost = cost
    self.action2 = action2
    self.attack = attack

MotherSupply = []
selectSetList = ['海辺','基本','異郷','陰謀']#抽選対象の拡張セット
attackNeed = 3#アタックの最低枚数
action2Need = 1#+2アクションの最低枚数
LowCostsNeed = 3#コスト3以下の最低枚数
HighCostsNeed = 3#コスト5以上の最低枚
EachSetNeed = [0,0,0,5]#各セットの最低枚数]
SetDict = {'基本':0,'陰謀':1,'海辺':2,'異郷':3}

for data in data.itertuples():
    if data[1] in selectSetList:
      MotherSupply.append(Card(data[0],data[1],data[2],data[3],data[4],data[5]))

dataSize = len(MotherSupply)
choiseSize = 10#サプライ生成枚数
print('総データ：'+ str(dataSize) + '  選択数: ' + str(choiseSize))

finish = False

while finish == False:
  Supply =[]
  randomizer = random.sample(range(dataSize), choiseSize)
  for i in randomizer:
    Supply.append(MotherSupply[i])

  finish = False  
  attackCount = 0
  action2Count = 0
  LowCostsCount = 0
  HighCostsCount = 0
  EachSetCount = [0,0,0,0]

  for i in Supply:
    if i.attack==1:
      attackCount += 1
    if i.action2==1:
      action2Count += 1
    if i.cost<=3:
      LowCostsCount+= 1
    if i.cost>=5:
      HighCostsCount+= 1
    EachSetCount[SetDict[i.exset]]+=1
  
  if attackCount>=attackNeed:
    if action2Count>=action2Need:
      if LowCostsCount>=LowCostsNeed:
        if HighCostsCount>=HighCostsNeed:
            for i in range(4):
              if EachSetCount[i]<EachSetNeed[i]:
                break
              if i == 3:
                finish = True

showSupply=[[],[],[],[]]

for i in Supply:
  for j in range(4):
    if SetDict[i.exset]==j:
      showSupply[j].append(i.name + '(' + str(i.cost) + ')' )

for i in range(4):
  CardString =''
  for j in showSupply[i]:
    CardString += '   ' + j
  print(str(list(SetDict)[i]) + ' :' + CardString)

