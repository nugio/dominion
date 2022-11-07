#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import pandas as pd 
import random


def pushed(b):
 b["text"] = "pushed"
 ChecksListUp()

#rootウィンドウを作成
root = tk.Tk()
#rootウィンドウのタイトルを変える
root.title("Tkinterテスト")
#rootウィンドウの大きさを320x240に
root.geometry("500x500")

def MakeSupply():
    
    data= pd.read_csv('pytest.csv' , encoding="shift-jis")

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


#Label部品を作る
label = tk.Label(root, text="Tkinterのテストです")
label.pack()

VarExsetList =[]
for i in range(4):
    VarExsetList.append(tk.BooleanVar())

CheckBox1 = tk.Checkbutton(text=u"基本",variable=VarExsetList[0])
CheckBox1.pack()
CheckBox2 = tk.Checkbutton(text=u"陰謀",variable=VarExsetList[1])
CheckBox2.pack()
CheckBox3 = tk.Checkbutton(text=u"海辺",variable=VarExsetList[2])
CheckBox3.pack()
CheckBox4 = tk.Checkbutton(text=u"異郷",variable=VarExsetList[3])
CheckBox4.pack()

def ChecksListUp():
    returnList = []
    for i in range(4):
        if VarExsetList[i].get() == True:
            returnList.append(1)
        else:
            returnList.append(0)        
    print(returnList)

    

#ボタンを作る
button = tk.Button(root, text="チェック読み", command= lambda : pushed(button))
#表示
button.pack()


#ボタン2
button2 = tk.Button(root, text="サプライ生成", command= lambda : MakeSupply())
button2.pack()

#メインループ
root.mainloop()

def supplytest(joken):
    if joken==1:
        return '1です'
    elif joken==2:
        return '2です'




