from pymongo import MongoClient
import math

client = MongoClient() # 接続先を指定Localhostの場合はvoidで良い
db = client['calcMass'] # データベースを選択

def calcExactMass(mw):
    # パラメーターの初期設定
    # inputMass = 170 # input Exact mass
    # number of ~ noc, noh 元素数
    # 元素の最大値
    elementMax = {'c' : 100, 'h' : 200, 'o' : 30, 'n' : 30}
    # 原子量
    atomicWeight = {'c' : 12, 'h' : 1.00782503, 'o' : 15.9949146, 'n' : 14.003074 }

    # 元素の最大数の絞り込み
    if mw / atomicWeight['c'] < elementMax['c'] :
        elementMax['c'] = int( mw / atomicWeight['c'] )
    if mw / atomicWeight['h'] < elementMax['h'] :
        elementMax['h'] = int( mw / atomicWeight['h'] )
    if mw / atomicWeight['o'] < elementMax['o'] :
        elementMax['o'] = int( mw / atomicWeight['o'] )
    if mw / atomicWeight['n'] < elementMax['n'] :
        elementMax['n'] = int( mw / atomicWeight['n'] )

    # 分子量計算
    for noc in range(elementMax['c']):
        for noh in range(elementMax['h']):
            for noo in range(elementMax['o']):
                for non in range(elementMax['n']):
                    mz = noc * atomicWeight['c'] + noh * atomicWeight['h'] + noo * atomicWeight['o'] + non * atomicWeight['n']
                    # 理論値からのズレを計算 Delta
                    delta = math.fabs(mw - mz)
                    # 誤差の大きいものはデータベースに入れない
                    if delta <  1 :
                        rdb = (2 * noc + 2 - noh + non ) / 2
                        # Massの項目追加
                        db.Mass.insert({'ExactMass' : mz, 'C' : noc, 'H': noh, 'O' : noo, 'N': non, 'Rdb' : rdb, 'Delta' : delta })
    # Massのfind
    for data in db.Mass.find():
        print(data)
    return data

if __name__ == "__main__":
    mass = calcExactMass(170)
    print("---")
    print(mass)
    print("program end")
