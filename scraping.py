import csv

import requests
from bs4 import BeautifulSoup


def main():
    # 商品一覧ページを取得して解析
    base_url = "https://www.franklinplanner.co.jp/shopping/binder/"
    base_html = requests.get(base_url)
    base_soup = BeautifulSoup(base_html.content, "html.parser")

    # ページの内容から商品ページのリンクを取得
    p_itemn_list = base_soup.select('p.list_itemn')

    # 全商品のcsvデータを保持するリスト
    item_list_csv_list = []
    item_list_csv_list.append(
        ['商品名', 'URL', 'リング径', '本体', '重さ', '左', '右', '外側', '内側'])

    for p_itemn in p_itemn_list:
        # 商品のcsvデータを保持するリスト
        item_csv_list = []

        # リンクを取得
        a = p_itemn.find('a')

        # 商品名取得
        item_csv_list.append(a.text)

        # 商品ページへのURLを作成
        item_url = base_url + a.get('href')

        # 商品名取得
        item_csv_list.append(item_url)

        # 商品ページを取得して解析
        item_html = requests.get(item_url)
        item_soup = BeautifulSoup(item_html.content, "html.parser")

        # table.trタグ取得
        table = item_soup.find('table')
        tr_list = table.find_all('tr')

        # 商品情報取得
        for tr in tr_list:
            th = tr.find('th')
            td = tr.find('td')
            if th is not None and td is not None:
                item_csv_list.append(td.text.replace('\n', ''))

        # 全商品csvデータへ追加
        item_list_csv_list.append(item_csv_list)

    with open('item_csv_list.csv', 'w', encoding='shiftjis', newline='', errors='ignore') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
        writer.writerows(item_list_csv_list)


if __name__ == '__main__':
    main()
