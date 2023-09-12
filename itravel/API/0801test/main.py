from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
# from flask_jwt_extended import create_access_token, jwt_required
import travel_tinerary_model
from datetime import datetime
from main_function import get_table,get_traveldates,getdatetime
from random import randint
from flask import jsonify,request,Flask
import geopandas as gpd
from my_score import calculate_price_score, calculate_price_score_2, calculate_tag_score
from shapely.geometry import Point
import numpy as np
import pandas as pd

app = Flask(__name__)

kwargslist = ["departure_date","return_date","hotel_level","food_level","viewpoint_level","transportation","food_price_tag",\
              "hotel_price_tag","food_taste_tag","food_other_tag","hotel_like_tag","hotel_other_tag","viewpoint_other_tag"]

class Travel(MethodResource):
    @doc(description='Get travel itinerary info.', tags=['get'])
    @use_kwargs(travel_tinerary_model.travelGetSchema,location="query")
    @marshal_with(travel_tinerary_model.travelGetResponse, code=200)
    @app.route( "/Travel", methods=["GET"])
    def get():
        try:
            county = request.args["county"]
            dates = request.args["dates"]
            departure_date = datetime.strptime(request.args["departure_date"],"%Y-%m-%d")
            return_date = datetime.strptime(request.args["return_date"],"%Y-%m-%d")
            if dates != (return_date-departure_date).days+1: dates=(return_date-departure_date).days+1
            print(dates,(return_date-departure_date).days+1)
            
            get_travel,_ = get_traveldates(dates)
            food_select = f"select * from merged_table_rest_cata_0 where city = '{county}'"
            hotel_select = f"select * from hotel_open_data_v2 where city = '{county}'"
            okgo_tw_v2_select = f"select * from okgo_tw_v2 where city = '{county}'"
            
            df_food = get_table(food_select)
            df_hotel = get_table(hotel_select)
            df_okgo_tw_v2 = get_table(okgo_tw_v2_select)
           
            input_mustplace = get_travel.copy()
            input_mustplace = getdatetime(dates,departure_date,return_date,input_mustplace)
            
            for ind,_ in enumerate(input_mustplace):
                for k1,v1 in input_mustplace[ind][f"day{ind+1}"][1].items():
                    if (v1==None) and (k1 in ["lunch","dinner"]):
                        if not df_food.empty:
                            df_go=df_food.iloc[randint(0,df_food.shape[0]-1)]
                            input_mustplace[ind][f"day{ind+1}"][1][k1]={"name":df_go["name"]}
                            input_mustplace[ind][f"day{ind+1}"][1][k1].update({"address":df_go["address"]})
                            input_mustplace[ind][f"day{ind+1}"][1][k1].update({"city":df_go["city"]})
                            df_gotime=df_go["time"].split(",")
                            df_gotime1=[]
                            for _,v in enumerate(df_gotime):
                                v = v.replace('\"',"").replace('\"',"").replace(" ","").strip("[").strip("]")
                                df_gotime1.append(v)
                            input_mustplace[ind][f"day{ind+1}"][1][k1].update({"time":df_gotime1})
                            input_mustplace[ind][f"day{ind+1}"][1][k1].update({"lat":float(df_go["lat"])})
                            input_mustplace[ind][f"day{ind+1}"][1][k1].update({"lng":float(df_go["lng"])})
                            input_mustplace[ind][f"day{ind+1}"][1][k1].update({"star":df_go["star"]})
                        else:
                            input_mustplace[ind][f"day{ind+1}"][1][k1] = None
                        
                    elif (v1==None) and (k1 == "hotel"): 
                        df_go=df_hotel.iloc[randint(0,df_hotel.shape[0]-1)]
                        input_mustplace[ind][f"day{ind+1}"][1][k1]={"name":df_go["name"]}
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"address":df_go["address"]})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"city":df_go["city"]})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"lat":float(df_go["lat"])})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"lng":float(df_go["lng"])})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"phone":df_go["phone"]})

                    elif (v1==None) and (k1 in ["morning_time","afternoon_time1","afternoon_time2"]): 
                        df_go=df_okgo_tw_v2.iloc[randint(0,df_okgo_tw_v2.shape[0]-1)]
                        input_mustplace[ind][f"day{ind+1}"][1][k1]={"name":df_go["name"]}
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"city":df_go["city"]})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"lat":float(df_go["lat"])})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"lng":float(df_go["lng"])})
                        input_mustplace[ind][f"day{ind+1}"][1][k1].update({"introduce":df_go["introduce"]})


            return jsonify({"message":input_mustplace,"state":2}) 
                
        except(ValueError)as e:
            error_message = str(e)
            index_of_error = error_message.find(''' (0x27) at index ''')
            return jsonify({"message": f"Caught ValueError: {error_message} at index {index_of_error}", "state": 0})
        except(KeyError)as e:
            return jsonify({"message":f"缺少必要的參數: {e}","state":0})

    @doc(description='Get travel itinerary info.', tags=['post'])
    @use_kwargs(travel_tinerary_model.travelPostSchema)
    @marshal_with(travel_tinerary_model.travelPostResponse, code=200)
    @app.route( "/Travel", methods=["POST"])
    def post():
        try:
            kwargs = request.json
            print("Received JSON data:", kwargs)
            for i,v in enumerate(kwargslist) :
                if len(kwargs.keys()) == 15: break
                if v not in kwargs.keys() and i <=7:  kwargs.update({kwargslist[i]:0})
                elif v not in kwargs.keys() and i >7:  kwargs.update({kwargslist[i]:[]})
            print(kwargs)

            # if (kwargs["return_date"] and kwargs["departure_date"]) != 0:
            #     departure_date = datetime.strptime(kwargs["departure_date"],"%Y-%m-%d")
            #     return_date = datetime.strptime(kwargs["return_date"],"%Y-%m-%d")
            #     if kwargs["dates"] != (return_date-departure_date).days+1: kwargs["dates"]=(return_date-departure_date).days+1
            # else: departure_date = return_date = 0
            # get_travel,times = get_traveldates(kwargs["dates"])
            # get_travel = getdatetime(kwargs["dates"],get_travel,departure_date,return_date)
            # 添加确认参数是否存在的代码
            # if 'hotel_price_tag' not in kwargs:
            #     return jsonify({"message": "缺少必要的參數: hotel_price_tag", "state": 0})

            # if 'food_price_tag' not in kwargs:
            #     return jsonify({"message": "缺少必要的參數: food_price_tag", "state": 0})

            # # 确认参数的值是否有效
            # if not isinstance(kwargs['hotel_price_tag'], int):
            #     return jsonify({"message": "参数 hotel_price_tag 的值必须为整数类型", "state": 0})

            # if not isinstance(kwargs['food_price_tag'], int):
            #     return jsonify({"message": "参数 food_price_tag 的值必须为整数类型", "state": 0})

            departure_date = 0
            return_date = 0

            if kwargs["return_date"] and kwargs["departure_date"]:
                departure_date = datetime.strptime(kwargs["departure_date"], "%Y-%m-%d")
                return_date = datetime.strptime(kwargs["return_date"], "%Y-%m-%d")
                if kwargs["dates"] != (return_date - departure_date).days + 1:
                    kwargs["dates"] = (return_date - departure_date).days + 1

            get_travel, times = get_traveldates(kwargs["dates"])

            # 确保调用 getdatetime() 前 departure_date 和 return_date 已经定义
            if departure_date and return_date:
                get_travel = getdatetime(kwargs["dates"], get_travel, departure_date, return_date)
            # 資料庫
            food_select = f"select * from rest_tag where city = '{kwargs['county']}'"
            hotel_select = f"select * from hotel_open_data_v3 where city = '{kwargs['county']}'"
            viewpoint_select = f"select * from okgo_tw_v2 where city = '{kwargs['county']}'"

            df_viewpoint = get_table(viewpoint_select)
            df_viewpoint = gpd.GeoDataFrame(df_viewpoint, crs="EPSG:4326", geometry=[Point(lnglat) for lnglat in zip(df_viewpoint['lng'], df_viewpoint['lat'])])

            df_food = get_table(food_select)

            # df_food['price_level'] = df_food['price_level'].astype(int)
            # kwargs['food_price_tag'] = int(kwargs['food_price_tag'])
            df_food['price_level'] = df_food['price_level'].fillna(-1).astype(int)
            # df_food['pref_price_level'] = df_food['pref_price_level'].fillna(-1).astype(int)

            df_food = gpd.GeoDataFrame(df_food, crs="EPSG:4326", geometry=[Point(lnglat) for lnglat in zip(df_food['lng'], df_food['lat'])])

            df_hotel = get_table(hotel_select)
            df_hotel['lng'] = pd.to_numeric(df_hotel['lng'], errors='coerce')
            df_hotel['lat'] = pd.to_numeric(df_hotel['lat'], errors='coerce')

            df_hotel = gpd.GeoDataFrame(df_hotel, crs="EPSG:4326", geometry=[Point(lnglat) for lnglat in zip(df_hotel['lng'], df_hotel['lat'])])
            print(kwargs['hotel_price_tag'])
     

            print(df_hotel['lower_price'].dtype)
            print(df_hotel['ceiling_price'].dtype)

            # 給Hotel分數
            df_hotel['like_score'] = calculate_tag_score(df_hotel['keyword'], kwargs["hotel_like_tag"])
            df_hotel['price_score'] = calculate_price_score(df_hotel['lower_price'], df_hotel['ceiling_price'], kwargs['hotel_price_tag'])
            df_hotel['other_score'] = calculate_tag_score(df_hotel['tag'], kwargs["hotel_other_tag"])

            # 計算Hotel加權平均分數 
            weights = pd.Series([0.4, 0.3, 0.3])
            df_hotel['overall_score'] = np.average(df_hotel[['like_score', 'price_score', 'other_score']], axis=1, weights=weights)

            # 給Food分數

            df_food['taste_score'] = calculate_tag_score(df_food['tag'], kwargs["food_taste_tag"])
            df_food['price_score'] = calculate_price_score_2(df_food['price_level'], kwargs['food_price_tag'])
            df_food['other_score'] = calculate_tag_score(df_food['tag2'], kwargs["food_other_tag"])

            # 計算Food加權平均分數 
            weights = pd.Series([0.4, 0.3, 0.3])
            df_food['overall_score'] = np.average(df_food[['taste_score', 'price_score', 'other_score']], axis=1, weights=weights)

            # 給ViewPoint分數
            df_viewpoint['other_score'] = 100
            df_viewpoint['transportation_score'] = 100

            # 計算ViewPoint加權平均分數 
            weights = pd.Series([0.4, 0.6])
            df_viewpoint['overall_score'] = np.average(df_viewpoint[['other_score', 'transportation_score']], axis=1, weights=weights)

            df_hotel = df_hotel.sort_values(by='overall_score', ascending=False).head(times["hotel"])
            df_hotel["use"] = 0
            df_food = df_food.sort_values(by='overall_score', ascending=False).head(times["food"])
            df_food["use"] = 0
            df_viewpoint = df_viewpoint.sort_values(by='overall_score', ascending=False).head(times["view"])
            df_viewpoint["use"] = 0
            
            for ind,_ in enumerate(get_travel):
                for k1,v1 in get_travel[ind][f"day{ind+1}"][1].items():
                    if (v1==None) and (k1 in ["lunch","dinner"]):
                        if not df_food.empty:
                            df_go=df_food[df_food["use"]==0]
                            df_go = df_go.iloc[randint(0,df_go.shape[0]-1)]
                            df_food.loc[df_go["name"] == df_food["name"],"use"] = 1
                            get_travel[ind][f"day{ind+1}"][1][k1]={"name":df_go["name"]}
                            get_travel[ind][f"day{ind+1}"][1][k1].update({"address":df_go["address"]})
                            get_travel[ind][f"day{ind+1}"][1][k1].update({"city":df_go["city"]})
                            df_gotime=df_go["time"].split(",")
                            df_gotime1=[]
                            for _,v in enumerate(df_gotime):
                                v = v.replace('\"',"").replace('\"',"").replace(" ","").strip("[").strip("]")
                                df_gotime1.append(v)
                            get_travel[ind][f"day{ind+1}"][1][k1].update({"time":df_gotime1})
                            get_travel[ind][f"day{ind+1}"][1][k1].update({"lat":float(df_go["lat"])})
                            get_travel[ind][f"day{ind+1}"][1][k1].update({"lng":float(df_go["lng"])})
                            get_travel[ind][f"day{ind+1}"][1][k1].update({"star":df_go["star"]})
                        else:
                            get_travel[ind][f"day{ind+1}"][1][k1] = None
                        
                    elif (v1==None) and (k1 == "hotel"): 
                        df_go=df_hotel[df_hotel["use"]==0]
                        df_go = df_go.iloc[randint(0,df_go.shape[0]-1)]
                        df_hotel.loc[df_go["name"] == df_hotel["name"],"use"] = 1
                        get_travel[ind][f"day{ind+1}"][1][k1]={"name":df_go["name"]}
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"address":df_go["address"]})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"city":df_go["city"]})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"lat":float(df_go["lat"])})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"lng":float(df_go["lng"])})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"phone":df_go["phone"]})

                    elif (v1==None) and (k1 in ["morning_time","afternoon_time1","afternoon_time2"]): 
                        df_go=df_viewpoint[df_viewpoint["use"]==0]
                        df_go = df_go.iloc[randint(0,df_go.shape[0]-1)]
                        df_viewpoint.loc[df_go["name"] == df_viewpoint["name"],"use"] = 1
                        get_travel[ind][f"day{ind+1}"][1][k1]={"name":df_go["name"]}
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"city":df_go["city"]})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"lat":float(df_go["lat"])})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"lng":float(df_go["lng"])})
                        get_travel[ind][f"day{ind+1}"][1][k1].update({"introduce":df_go["introduce"]})


            return jsonify({"message":get_travel,"state":2}) 
                
        except(ValueError)as e:
            app.logger.error("Caught exception in post() function:", exc_info=True)        
            error_message = str(e)
            index_of_error = error_message.find(''' (0x27) at index ''')
            return jsonify({"message": f"Caught ValueError: {error_message} at index {index_of_error}", "state": 0})
        except(KeyError)as e:
            return jsonify({"message":f"缺少必要的參數: {e}","state":0})
        # except :
        #     return jsonify({"message":f"ValueError以及KeyError以外之錯誤","state":0})
            error_message = str(e)
            index_of_error = error_message.find(''' (0x27) at index ''')
            return jsonify({"message": f"Caught ValueError: {error_message} at index {index_of_error}", "state": 0})
        except(KeyError)as e:
            return jsonify({"message":f"缺少必要的參數: {e}","state":0})
        # except :
        #     return jsonify({"message":f"ValueError以及KeyError以外之錯誤","state":0})