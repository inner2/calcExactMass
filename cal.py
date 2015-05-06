from pymongo import MongoClient
import math

client = MongoClient()  # 接続先を指定Localhostの場合はvoidで良い
db = client['calcMass']  # データベースを選択


def calc_exact_mass(mw):
    # パラメーターの初期設定
    # inputMass = 170 # input Exact mass
    # number of ~ noc, noh 元素数
    # 元素の最大値
    element_max = {'c': 100, 'h': 200, 'o': 30, 'n': 30}
    # 原子量
    atomic_weight = {'c': 12, 'h': 1.00782503, 'o': 15.9949146, 'n': 14.003074}

    # 元素の最大数の絞り込み
    if mw / atomic_weight['c'] < element_max['c']:
        element_max['c'] = int(mw / atomic_weight['c'])
    if mw / atomic_weight['h'] < element_max['h']:
        element_max['h'] = int(mw / atomic_weight['h'])
    if mw / atomic_weight['o'] < element_max['o']:
        element_max['o'] = int(mw / atomic_weight['o'])
    if mw / atomic_weight['n'] < element_max['n']:
        element_max['n'] = int(mw / atomic_weight['n'])

    # 分子量計算
    for noc in range(element_max['c']):
        for noh in range(element_max['h']):
            for noo in range(element_max['o']):
                for non in range(element_max['n']):
                    mz = noc * atomic_weight['c'] + noh * atomic_weight['h'] + noo * atomic_weight['o'] + non * atomic_weight['n']
                    # 理論値からのズレを計算 Delta
                    delta = math.fabs(mw - mz)
                    # 誤差の大きいものはデータベースに入れない
                    if delta < 1:
                        rdb = (2 * noc + 2 - noh + non) / 2
                        # Massの項目追加
                        db.Mass.insert({'ExactMass': mz, 'C': noc, 'H': noh, 'O': noo, 'N': non, 'Rdb': rdb, 'Delta': delta })
    # Massのfind
    query = db.Mass.find()
    for data in query:
        print(data)
    return query

if __name__ == "__main__":
    mass = calc_exact_mass(170)
    print("---")
    print(mass)
    print("program end")
