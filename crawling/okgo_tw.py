import requests
from bs4 import BeautifulSoup
from random import randint
import json
import time

def okgo_data():
    data = []
    for i in range(1, 4300):
        url = "https://okgo.tw/butyview.html?id=" + str(i)
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("div", class_="sec3 word Resize")
        if result:
            district = result.text.split()[5:][0]
            print(district)
        else:
            print("未找到其他信息")
            continue
        name_ = result.text.split()[5:][1]
        print(name_)
        address = result.text.split()[5:][3][3:]
        print(address)
        introduce = result.text.split()[5:][-1]
        print(introduce)
        traffic = soup.find("div", id="Buty_View_Traffic").text.split()
        print(traffic)
        hot = soup.find("ul", class_="dot").text.split()
        print(hot)
        item = {
            "district": district,
            "name": name_,
            "address": address,
            "introduce": introduce,
            "traffic": traffic,
            "hot": hot
        }
        data.append(item)
        print("爬完第", i, "頁")
        time.sleep(randint(3, 7))

    grouped_data = {}
    for item in data:
        district = item['district']
        content = item
        if district not in grouped_data:
            grouped_data[district] = [content]
        else:
            grouped_data[district].append(content)


    with open (f"okgo_tw.json","w",encoding="utf8") as f:
        json.dump(grouped_data,f,ensure_ascii=False)

if __name__ == "__main__":
    okgo_data()
