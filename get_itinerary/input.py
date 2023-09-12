# API travel_tinerary_model:
# county = fields.Str(example="台北市",required=True)               # 先單選(之後再考慮是否改成多選)
# dates = fields.Int(example=2,required=True)                       # 1~7
# departure_date = fields.Str(example="2023-07-24",required=True)   # 改成非必填? date跟區間2擇一?
# return_date = fields.Str(example="2023-07-25",required=True)      # 改成非必填? date跟區間2擇一?

# hotel_level = fields.Int(example=5)         # 1~5
# food_level = fields.Int(example=5)          # 1~5
# viewpoint_level = fields.Int(example=5)     # 1~5

# hotel_like_tag = fields.Str(example=["民宿", "汽車旅館"])    # 多選(list): 飯店/旅館/酒店, 汽車旅館, 民宿, 青年/背包旅館
# hotel_price_tag = fields.Int(example=2000)                  # 1000~9000
# hotel_other_tag = fields.Str(example=["SPA", "停車場"])      # 多選(list): SPA, 停車場 ...

# food_taste_tag = fields.Str(example=["燒烤", "日式", "韓式"])  # 多選(list): 燒烤, 日本料理, 韓式料理, 火鍋, 泰式料理, 鐵板燒, 速食餐廳, 宵夜, 小吃, 居酒屋, 川菜
# food_price_tag = fields.Int(example=2)                        # 1~5
# food_other_tag = fields.Str(example=["親子餐廳"])              # 多選(list):親子餐廳, 約會餐廳, 精緻高級

# viewpoint_other_tag = fields.Str(example=["戶外活動"])       # 多選(list):  戶外活動, 海洋, ... 
# transportation = fields.Int(example=1)                      # 1:True 0:False

#######################
# JSON格式範例資料
#######################

pref = {
    "county": "嘉義市",
    "dates": 2,
    "departure_date": "2023-07-24",
    "return_date": "2023-07-25",

    "hotel_level": 5,
    "food_level": 5,
    "viewpoint_level": 5,

    "hotel_like_tag": ["民宿", "汽車旅館"],
    "hotel_price_tag": 2000,
    "hotel_other_tag": ["SPA", "停車場"],

    "food_taste_tag": ["燒烤", "日式", "韓式"],
    "food_price_tag": 2,
    "food_other_tag": ["親子餐廳"],

    "viewpoint_other_tag": ["戶外活動"],
    "transportation": 1,
}
