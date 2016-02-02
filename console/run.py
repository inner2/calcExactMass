# python3
# Module
import sqlite3
import math

# Connect database
conn = sqlite3.connect(':memory:')
c = conn.cursor()

# パラメーターの初期設定
element_max = {'c': 100, 'h': 200, 'o': 30, 'n': 30}  # 元素の最大値
atomic_weight = {'c': 12, 'h': 1.00782503, 'o': 15.9949146, 'n': 14.003074}  # 原子量
delta_range = 1  # 誤差の範囲 delta の絞り込み範囲
result_limit = 15  # 結果の表示数


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
                        c.execute("insert into stocks values(?, ?, ?, ?, ?, ?, ?, ?)", (formula, mw, noc, noh, noo, non, rdb, delta))

    # Massのfind
    # データの抽出
    c.execute("select * from stocks order by delta asc limit '" + str(result_limit) + "'")
    result_list = c.fetchall()
    for result in result_list:
        print(result)


# DB create table
def db_table_create():
    # テーブルの作成
    c.execute("create table stocks(Formula, ExactMass, c, h, o, n, rdb, delta)")


# DB close
def db_close():
    # Save
    # conn.save()
    # Close
    conn.close()


if __name__ == "__main__":
    db_table_create()
    print(" m/z ?")
    mz = input()
    calc_exact_mass(float(mz))
    db_close()