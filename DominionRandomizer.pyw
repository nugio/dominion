#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import pandas as pd 
import random

#rootウィンドウを作成
root = tk.Tk()
root.title("ドミニオン　サプライ生成")
root.geometry("800x380")

def MakeSupply(optionDict):#サプライ生成のメイン関数
    
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
    selectSetList = optionDict['selectSetList']#抽選対象の拡張セット
    attackNeed = optionDict['attackNeed']#アタックの最低枚数
    action2Need = optionDict['action2Need']#+2アクションの最低枚数
    LowCostsNeed = optionDict['LowCostsNeed']#コスト3以下の最低枚数
    HighCostsNeed = optionDict['HighCostsNeed']#コスト5以上の最低枚
    EachSetNeed = optionDict['EachSetNeed']#各セットの最低枚数]
    SetDict = {'基本':0,'陰謀':1,'海辺':2,'異郷':3}

    for data in data.itertuples():
        if data[1] in selectSetList:
            MotherSupply.append(Card(data[0],data[1],data[2],data[3],data[4],data[5]))

    dataSize = len(MotherSupply)
    choiseSize = 10#サプライ生成枚数
    #print('総データ：'+ str(dataSize) + '  選択数: ' + str(choiseSize))

    finish = False
    tryCount = 0

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

        for card in Supply:
            if card.attack==1:
                attackCount += 1
            if card.action2==1:
                action2Count += 1
            if card.cost<=3:
                LowCostsCount+= 1
            if card.cost>=5:
                HighCostsCount+= 1
            EachSetCount[SetDict[card.exset]]+=1
        
        if attackCount>=attackNeed:
            if action2Count>=action2Need:
                if LowCostsCount>=LowCostsNeed:
                    if HighCostsCount>=HighCostsNeed:
                        for i in range(4):
                            if EachSetCount[i]<EachSetNeed[i]:
                                break
                            if i == 3:
                                finish = True
        tryCount+=1

        if tryCount>50000:
            if txtBox.get('1.0',tk.END):
                txtBox.delete('1.0',tk.END)
            txtBox.insert(tk.END,'その組み合わせは無いみたい・・・')
            return            

    showSupply=[[],[],[],[]]

    for card in Supply:
        for j in range(4):
            if SetDict[card.exset]==j:
               showSupply[j].append(card.name + '(' + str(card.cost) + ')' )

    showtext =''
    for i in range(4):
        CardString =''
        for j in showSupply[i]:
            CardString += '  ' + j
        if CardString !='':
            showtext += str(list(SetDict)[i]) + ':' + CardString + '\n\n\n'
    
    if txtBox.get('1.0',tk.END):
        txtBox.delete('1.0',tk.END)
    txtBox.insert(tk.END,showtext)

label = tk.Label(root, text="使用する拡張")
label.place(x=20, y=15)

VarExsetList =[]
for i in range(4):
    VarExsetList.append(tk.BooleanVar())
    VarExsetList[i].set(1)

CheckBox1 = tk.Checkbutton(text="基本",variable=VarExsetList[0])
CheckBox1.place(x=25, y=40)
CheckBox2 = tk.Checkbutton(text="陰謀",variable=VarExsetList[1])
CheckBox2.place(x=25, y=70)
CheckBox3 = tk.Checkbutton(text="海辺",variable=VarExsetList[2])
CheckBox3.place(x=25, y=100)
CheckBox4 = tk.Checkbutton(text="異郷",variable=VarExsetList[3])
CheckBox4.place(x=25, y=130)

label2 = tk.Label(root, text="最低枚数")
label2.place(x=130, y=15)

#枚数指定スピンボックス
VarspinboxList =[]
spinboxList=[]
for i in range(4):
    VarspinboxList.append(tk.StringVar())
    VarspinboxList[i].set(0)
    spinboxList.append(tk.Spinbox(root,width=3, from_=0, to=6, increment=1, textvariable=VarspinboxList[i]))
    spinboxList[i].place(x=140, y=45+i*30)

def optionToDict():

    SetDict = {'基本':0,'陰謀':1,'海辺':2,'異郷':3}
    revSetDict = {0:'基本',1:'陰謀',2:'海辺',3:'異郷'}
    optionDict = {}

    #抽選対象セットを取得
    returnList = []
    for i in range(4):
        if VarExsetList[i].get() == True:
            returnList.append(revSetDict[i])  
    if returnList==[]:
        if txtBox.get('1.0',tk.END):
                txtBox.delete('1.0',tk.END)
        txtBox.insert(tk.END,'どのセットも選択されてないよ・・・')
        return
    optionDict['selectSetList']=returnList   
    
    #枚数指定の取得
    SetNeedList=[]
    for i in range(4):
        SetNeedList.append(int(VarspinboxList[i].get()))
    optionDict['EachSetNeed']=SetNeedList

    #アタック、アクションの最低枚数指定
    optionDict['attackNeed']=attack.get()
    optionDict['action2Need']=action2.get()

    #コストバランスの指定
    if cost.get()==0:
        optionDict['LowCostsNeed']=0
        optionDict['HighCostsNeed']=0
    elif cost.get()==1:
        optionDict['LowCostsNeed']=4
        optionDict['HighCostsNeed']=0
    elif cost.get()==2:
        optionDict['LowCostsNeed']=0
        optionDict['HighCostsNeed']=4
    elif cost.get()==3:
        optionDict['LowCostsNeed']=3
        optionDict['HighCostsNeed']=3    
    
    MakeSupply(optionDict) #Dictを引数で渡し、検索起動

#サプライ生成ボタン
button2 = tk.Button(root, text="サプライ生成",width=25,height=3, command= lambda : optionToDict())
button2.place(x=300, y=160)

# +2アクションのラジオボタン
action2 = tk.IntVar()
action2.set(0)# 初期値value=0
label = tk.Label(root, text="+2アクション")
label.place(x=230, y=15)
act1 = tk.Radiobutton(root, value=0, variable=action2, text='何でも')
act1.place(x=230, y=40)
act2 = tk.Radiobutton(root, value=1, variable=action2, text='含む')
act2.place(x=230, y=60)
act3 = tk.Radiobutton(root, value=2, variable=action2, text='多め')
act3.place(x=230, y=80)

# アタックのラジオボタン
attack = tk.IntVar()
attack.set(0)# 初期値value=0
label = tk.Label(root, text="アタック")
label.place(x=330, y=15)
atk1 = tk.Radiobutton(root, value=0, variable=attack, text='何でも')
atk1.place(x=330, y=40)
atk2 = tk.Radiobutton(root, value=1, variable=attack, text='含む')
atk2.place(x=330, y=60)
atk3 = tk.Radiobutton(root, value=2, variable=attack, text='多め')
atk3.place(x=330, y=80)

# コストのラジオボタン
cost = tk.IntVar()
cost.set(0)# 初期値value=0
label = tk.Label(root, text="コスト")
label.place(x=430, y=15)
cost1 = tk.Radiobutton(root, value=0, variable=cost, text='何でも')
cost1.place(x=430, y=40)
cost2 = tk.Radiobutton(root, value=1, variable=cost, text='低コスト寄り (コスト3以下が最低4枚)')
cost2.place(x=430, y=60)
cost3 = tk.Radiobutton(root, value=2, variable=cost, text='高コスト寄り (コスト5以上が最低4枚)')
cost3.place(x=430, y=80)
cost4 = tk.Radiobutton(root, value=3, variable=cost, text='バランス     (ともに最低3枚)')
cost4.place(x=430, y=100)

label = tk.Label(root, text="サプライ")
label.place(x=10, y=200)

txtBox = tk.Text()
txtBox.configure(width=110,height=10)
txtBox.place(x=10, y=230)

#メインループ
root.mainloop()



