import random
import json
from datetime import datetime, timedelta

for k in range(10):
    counties = [
        '基隆市', '臺北市', '新北市', '桃園市', '新竹市', '新竹縣', '苗栗縣',
        '臺中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '臺南市',
        '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣'
    ]
    rest_tag = ["火鍋","燒烤","海鮮","酒","台式","日式","韓式","異國風味","中式港式","美式義式"]  # 餐廳tag可以加在這裡
    rest_tag2 = ['親子餐廳','寵物友善','素食'] 

    hotel_tag = ['飯店/旅館/酒店','青年/背包旅館','汽車旅館','民宿']  # hotel tag 可以加在這裡
    hotel_tag2 = ['自行車友善旅宿','無線網路','停車場','接送服務','洗衣服務','健身房']

    spot_tags = ['自然生態','文化藝術','農村景觀','風景遊憩','建築人文']  # spot tag 可以加在這裡

    # choose city
    city = random.choice(counties)
    departure_date = datetime.now() + timedelta(days=random.randint(1, 30))
    return_date = departure_date + timedelta(days=random.randint(1, 7))
    
    # choose hotel tag
    hotel_level = random.randint(1, 5)
    hotel_like_tag = random.sample(hotel_tag, 1)
    hotel_price_tag = random.randint(1000, 10000)
    hotel_other_tag = random.sample(hotel_tag2, 1)

    # choose restaurant tag
    food_level = random.randint(1, 5)
    food_taste_tag = random.sample(rest_tag, 2)
    food_price_tag = random.randint(1, 5)
    food_other_tag = random.sample(rest_tag2, 1)

    # choose viewpoint tag
    viewpoint_level = random.randint(1, 5)
    viewpoint_other_tag = random.sample(spot_tags, 1)

    transportation = random.randint(1, 2)

    # Generate the output dictionary
    pref = {
        "county": city,
        "dates": (return_date - departure_date).days,
        "departure_date": departure_date.strftime('%Y-%m-%d'),
        "return_date": return_date.strftime('%Y-%m-%d'),

        "hotel_level": hotel_level,
        "food_level": food_level,
        "viewpoint_level": viewpoint_level,

        "hotel_like_tag": hotel_like_tag,
        "hotel_price_tag": hotel_price_tag,
        "hotel_other_tag": hotel_other_tag,

        "food_taste_tag": food_taste_tag,
        "food_price_tag": food_price_tag,
        "food_other_tag": food_other_tag,

        "viewpoint_other_tag": viewpoint_other_tag,
        "transportation": transportation,
    }

    print(json.dumps(pref, ensure_ascii=False, indent=4))

    # Write to file
    filename = f"output_{k}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(pref, f, ensure_ascii=False, indent=4)
