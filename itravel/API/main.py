from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
# from flask_jwt_extended import create_access_token, jwt_required
import travel_tinerary_model
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
from random import choice,randint
from collections import Counter
from flask import Flask, jsonify, request

engine = create_engine("mysql+pymysql://ivy:000000@35.187.155.171/travel")
star_level = [3.5,3.7,4.0,4.3,4.5]

def get_table(args):
    """
    依需求連結指定table取值，並放入pandas。 
    """
    df = pd.read_sql(args,engine)
    return df
    
def get_traveldates(date):
    """
    依照天數安排每天應有行程數及行程格式，並統計各type的數量。
    """
    days = []
    for i in range(date):
        if date<=1 and i+1 >= date:
            oneday = {f"day{i+1}":
                        {"morning_time":None,
                        "lunch":None,
                        "afternoon_time1":None,
                        "afternoon_time2":None,
                        "dinner":None}}
        elif i+1 == date:
            oneday = {f"day{i+1}":
                        {"morning_time":None,
                        "lunch":None,
                        "afternoon_time1":None,
                        "afternoon_time2":None}}
        else:
            oneday = {f"day{i+1}":
                        {"morning_time":None,
                        "lunch":None,
                        "afternoon_time1":None,
                        "afternoon_time2":None,
                        "dinner":None,
                        "hotel":None}}
        days.append(oneday)

    if len(days)==1:
        times = {"food":2,"hotel":0,"view":3,"active":3}
    else:
        times = {"food":(len(days)-1)*2+1,"hotel":len(days)-1,"view":len(days)*3,"active":len(days)*3}

    return days,times
    



class Travel(MethodResource):
    @doc(description="Get travel itinerary info.", tags=["travel itinerary"])
    @use_kwargs(travel_tinerary_model.travelPostSchema, location="query")
    @marshal_with(travel_tinerary_model.travelPostResponse, code=200)
    # @get_startplace
    #def post(self,**kwargs):
    def get(self,**kwargs):
        try:
            county = kwargs["county"]
            dates = kwargs["dates"]

            get_travel,times = get_traveldates(dates)           
            food_select = f"(select * from merged_table_rest_cata where city = '{county}')"
            hotel_select = f"(select * from hotel_open_data where address like '{county}%%')"
            okgo_tw_v2_select = f"(select * from okgo_tw_v2 where city = '{county}')"

            df_food = get_table(food_select)
            df_hotel = get_table(hotel_select)
            df_okgo_tw_v2 = get_table(okgo_tw_v2_select)

            
            input_mustplace = get_travel.copy()

            
            for ind,_ in enumerate(input_mustplace):
                for k1,v1 in input_mustplace[ind][f"day{ind+1}"].items():
                    if (v1==None) and (k1 in ["lunch","dinner"]):
                        if not df_food.empty:
                            input_mustplace[ind][f"day{ind+1}"][k1]=df_food.iloc[randint(0,df_food.shape[0]-1)]["name"]
                        else:
                            input_mustplace[ind][f"day{ind+1}"][k1] = None
                        input_mustplace[ind][f"day{ind+1}"][k1]=df_food.iloc[randint(0,df_food.shape[0]-1)]["name"]
                    elif (v1==None) and (k1 == "hotel"): 
                        input_mustplace[ind][f"day{ind+1}"][k1]=df_hotel.iloc[randint(0,df_hotel.shape[0]-1)]["name"]
                    elif (v1==None) and (k1 in ["morning_time","afternoon_time1","afternoon_time2"]): 
                        input_mustplace[ind][f"day{ind+1}"][k1]=df_okgo_tw_v2.iloc[randint(0,df_okgo_tw_v2.shape[0]-1)]["name"]

            return {"message":input_mustplace,"state":2} 
        except ValueError as e:
            error_message = str(e)
            index_of_error = error_message.find(''' (0x27) at index ''')
            return {"message": f"Caught ValueError: {error_message} at index {index_of_error}", "state": 0}

      #  except ValueError as e:
       #     return {"message": f"Caught ValueError: {repr(e)}", "state": 0}

        except KeyError as e:
            return {"message": f"缺少必要的參數: {str(e)}", "state": 0}

#app = Flask(__name__)

#@app.route('/Travel', methods=['POST'])
#def get_travel_plan():
 #   try:
  #      data = request.json  # 從請求中取得 JSON 格式的資料
   #     print(data)  # 打印接收到的數據，以確認格式和內容是否正確

        # 檢查必填欄位是否存在
    #    if 'county' not in data or 'dates' not in data:
     #       return jsonify({"message": "必填欄位 county 和 dates 不能為空", "state": 0})

      #  county = data['county']
       # dates = data['dates']
#        departure_date = data.get('departure_date', '')  # 取得選填欄位，若不存在則預設為空字串
 #       return_date = data.get('return_date', '')        # 取得選填欄位，若不存在則預設為空字串
        # 依據其他選填欄位依此類推...
#
        # 在這裡進行你的處理和計算，得到旅遊行程結果 travel_result
        # 例如：
        #travel_result = {
         #   'county': county,
          #  'dates': dates,
  #          'departure_date': departure_date,
  #          'return_date': return_date,
            # 其他計算出來的旅遊行程資料...
     #   }

        # 將 travel_result 字典轉換成 JSON 格式並回傳
 #       return jsonify(travel_result)

  #  except Exception as e:
   #     return jsonify({"message": f"Caught an error: {e}", "state": 0})











