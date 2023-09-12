import requests
from bs4 import BeautifulSoup
import json
import time
from random import randint
import pymysql,os
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://emmmmma0527:123456@127.0.0.1:3306/travel?charset=utf8")

def okgo_data(start_page=1):
    data = []
    for i in range(start_page, 4300):
        url = "https://okgo.tw/butyview.html?id=" + str(i)
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("div", class_="sec3 word Resize")
        if result:
            district = result.text.split()[5:][0]
            #print(district)
        else:
            print("未找到其他信息")
            continue
        name_ = result.text.split()[5:][1]
        #print(name_)
        address = result.text.split()[5:][3][3:]
        #print(address)
        introduce = result.text.split()[5:][-1]
        #print(introduce)
        traffic = soup.find("div", id="Buty_View_Traffic").text
        #print(traffic)
        item = {
            "district": district,
            "attractions_name": name_,
            "address": address,
            "introduce": introduce,
            "traffic": traffic
        }
        data.append(item)
        print("爬完第", i, "頁")
        time.sleep(randint(3, 7))
            
        # 將資料轉換為 DataFrame
        df = pd.DataFrame(data)

        # 將 DataFrame 存入資料庫
        df.to_sql('okgo_tw', con=engine, if_exists='append', index=False)

        # 每爬取一頁就保存一次數據
        with open("okgo_tw.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)

if __name__ == "__main__":
    okgo_data()

