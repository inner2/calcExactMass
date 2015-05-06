from pymongo import MongoClient
import math
from flask import Flask, render_template, request

app = Flask(__name__)

client = MongoClient()  # 接続先を指定Localhostの場合はvoidで良い
db = client['calcMass']  # データベースを選択


# パラメーターの初期設定
element_max = {'c': 100, 'h': 200, 'o': 30, 'n': 30}  # 元素の最大値
atomic_weight = {'c': 12, 'h': 1.00782503, 'o': 15.9949146, 'n': 14.003074}  # 原子量
delta_range = 1  # 誤差の範囲 delta の絞り込み範囲
result_limit = 15 # 結果の表示数

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
                    if delta < delta_range:
                        rdb = (2 * noc + 2 - noh + non) / 2
                        formula = "C" + str(noc) + "H" + str(noh) + "O" + str(noo) + "N" + str(non)
                        # Massの項目追加
                        db.Mass.insert({'Formula':formula, 'ExactMass': mw, 'C': noc, 'H': noh, 'O': noo, 'N': non, 'Rdb': rdb, 'Delta': delta })
    # Massのfind
    query = db.Mass.find()
    result = list(query.sort('Delta').limit(result_limit))
    return result


# flask
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        input_mass = request.form["text"]
        if input_mass:
            # データベースの削除
            client.drop_database(db)
            # 分子式の計算関数を実行
            mass = calc_exact_mass(int(input_mass))
            return render_template("calcMass.html", input = input_mass, results = mass)
    return render_template("calcMass.html", input = "none")

if __name__ == "__main__":
    app.run()
