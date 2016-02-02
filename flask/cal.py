from pymongo import MongoClient
import math

client = MongoClient()  # 接続先を指定Localhostの場合はvoidで良い
db = client['calcMass']  # データベースを選択

# パラメーターの初期設定
element_max = {'c': 100, 'h': 200, 'o': 30, 'n': 30}  # 元素の最大値
atomic_weight = {'c': 12, 'h': 1.00782503, 'o': 15.9949146, 'n': 14.003074}  # 原子量

# 分子量を計算する関数
def calc_exact_mass(mz):
    # number of ~ noc, noh 元素数
    # 分子量計算
    for noc in range(element_max['c']):
        mc = noc * atomic_weight['c']
        if mc > mz:
            break
        for noh in range(element_max['h']):
            mh = noh * atomic_weight['h']
            if mc + mh > mz:
                break
            for noo in range(element_max['o']):
                mo = noo * atomic_weight['o']
                if mc + mh + mo > mz:
                    break
                for non in range(element_max['n']):
                    mn = non * atomic_weight['n']

                    mw = mc + mh + mo + mn
                    # 理論値(mw)と実測値(mz)のズレを計算 Delta
                    delta = math.fabs(mw - mz)
                    # 誤差の大きいものはデータベースに入れない
                    if delta < 1:
                        rdb = (2 * noc + 2 - noh + non) / 2
                        formula = "C" + str(noc) + "H" + str(noh) + "O" + str(noo) + "N" + str(non)
                        # Massの項目追加
                        db.Mass.insert({'Formula':formula, 'ExactMass': mw, 'C': noc, 'H': noh, 'O': noo, 'N': non, 'Rdb': rdb, 'Delta': delta })
    # Massのfind
    query = db.Mass.find()
    res = list(query.sort('Delta').limit(10))
    return res

if __name__ == "__main__":
    res = calc_exact_mass(170)
    result = []
    for i in range(10):
        #result.append("Formula: " + str(res[i]['Formula']) + "  ExactMass: " + str(res[i]['ExactMass']) + "  Delta: " + str(res[i]['Delta']))
        result.append([res[i]['Formula'], res[i]['ExactMass'], res[i]['Delta']])
    print(result[0])
    print("program end")
