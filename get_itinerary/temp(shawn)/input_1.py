import random
import json
for k in range(10):
    counties = [
        '基隆市', '臺北市', '新北市', '桃園市', '新竹市', '新竹縣', '苗栗縣',
        '臺中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '臺南市',
        '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣',
        '連江縣'
    ]
    rest_tag = ['燒烤', '日本料理', '韓式料理', '火鍋', '泰式料理', '鐵板燒', '速食餐廳', '宵夜', '小吃', '居酒屋', '川菜']  # 餐廳tag可以加在這裡
    rest_tag2 = ['親子餐廳','約會餐廳','精緻高級'] 

    hotel_tag = ['飯店/旅館/酒店','青年/背包旅館','汽車旅館','民宿']  # hotel tag 可以加在這裡
    hotel_tag2 = ['SPA','停車場']

    spot_tags = ['戶外活動','海洋']  # spot tag 可以加在這裡

    # choose city
    city = random.choice(counties)
    print(city)

    # 旅遊天數
    days = random.randint(2, 7)
    print(type(days))

    # choose restaurant tag
    food_tag = random.sample(rest_tag,3)
    print(food_tag)
    food_tag2 = random.sample(rest_tag,1)
    print(food_tag2)

    # 餐廳
    rest_importance = random.randint(1,5)
    print(type(rest_importance))

    # 餐廳評分
    food_rating = round(random.uniform(1,5),1) # 生成一個rating介在1.0~5.0
    food_rating = "{:.1f}".format(food_rating) # 讓生成的整數出現1.0
    food_rating = float(food_rating)
    print(food_rating)

    # restanrant price
    price = random.randint(1,5)
    print(price)

    # choose hotel tag
    tag_hotel = random.sample(hotel_tag,1)
    print(tag_hotel)
    tag_hotel2 = random.sample(hotel_tag2,1)
    print(tag_hotel2)

    # hotel
    hotel_importance = random.randint(1,5)
    print(type(hotel_importance))

    # hotel price
    price_min = 100*random.randint(1,200)
    price_max = 100*random.randint(1,200)
    while price_max < price_min:
        price_max = 100*random.randint(1,200)
    print(price_min,price_max)

    # hotel 評分
    hotel_rating = round(random.uniform(1,5),1) # 生成一個rating介在1.0~5.0
    hotel_rating = "{:.1f}".format(hotel_rating) # 讓生成的整數出現1.0
    hotel_rating = float(hotel_rating)
    print(type(hotel_rating))

    tag_spot = random.sample(spot_tags,1)
    print(tag_spot)

    # 戶外活動
    spot_importance = random.randint(1,5)
    print(type(spot_importance))

    #  評分
    spot_rating = round(random.uniform(1,5),1) # 生成一個rating介在1.0~5.0
    spot_rating = "{:.1f}".format(spot_rating) # 讓生成的整數出現1.0
    spot_rating = float(spot_rating)
    print(type(spot_rating))

    # input
    pref = {}
    pref["basic_days"] = days
    pref["basic_city"] = city
    pref["food_importance"] = rest_importance
    pref["food_tag"] = food_tag
    pref["food_tag2"] = food_tag2
    pref["food_min_rating"] = food_rating
    pref["food_max_price"] = price
    pref["hotel_importance"] = hotel_importance
    pref["hotel_tag"] = tag_hotel
    pref["hotel_tag2"] = tag_hotel2
    pref["hotel_min_price"] = price_min 
    pref["hotel_max_price"] = price_max 
    pref["hotel_min_rating"] = hotel_rating
    pref["spot_importance"] = spot_importance
    pref["spot_tag"] = tag_spot
    pref["spot_min_rating"] = spot_rating
    print(pref)

    # 寫成檔案
    filename = f"input_{k}.txt"
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(pref,f,ensure_ascii=False,indent=4)