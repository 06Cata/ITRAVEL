from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
# from flask_jwt_extended import create_access_token, jwt_required
import travel_tinerary_model
from datetime import datetime
from main_function import get_traveldates,getdatetime
from flask import jsonify,request,Flask
from mainrun import mainrun

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保中文不会被转义为 Unicode 转义序列

kwargslist = ["departure_date","return_date","hotel_level","food_level","viewpoint_level","transportation","food_price_tag",\
              "hotel_price_tag","food_taste_tag","food_other_tag","hotel_like_tag","hotel_other_tag","viewpoint_other_tag"]

class Travel(MethodResource):
    @doc(description='Get travel itinerary info.', tags=['post'])
    @use_kwargs(travel_tinerary_model.travelPostSchema)
    @marshal_with(travel_tinerary_model.travelPostResponse, code=200)
    @app.route( "/Travel", methods=["POST"])
    def post():
        try:
            kwargs = request.json
            for i,v in enumerate(kwargslist) : 
                # if len(kwargs.keys()) == 15: break
                # if v not in kwargs.keys() and i <=7:  kwargs.update({kwargslist[i]:0})
                # elif v not in kwargs.keys() and i >7:  kwargs.update({kwargslist[i]:[]})
                if kwargs[v] == None and i <=7: kwargs[v] = 0

            print(kwargs)

            departure_date = return_date = 0
            if (kwargs["return_date"] and kwargs["departure_date"]) != 0:
                departure_date = datetime.strptime(kwargs["departure_date"],"%Y-%m-%d")
                return_date = datetime.strptime(kwargs["return_date"],"%Y-%m-%d")
                if kwargs["dates"] != (return_date-departure_date).days+1: kwargs["dates"]=(return_date-departure_date).days+1
           
            get_travel,_ = get_traveldates(kwargs["dates"])
            get_travel, weekday_name = getdatetime(kwargs["dates"],get_travel,departure_date,return_date)
            if weekday_name != 0 :
                weekday_name = [datetime.strptime(i,"%Y-%m-%d").strftime("%A") for i in weekday_name ]
            print(weekday_name)

            itinerary_df,concat_df = mainrun(kwargs,weekday_name)

            for ind in range(len(get_travel)):
                itinerary_df_day = itinerary_df[itinerary_df["day"] == ind+1]
                for i1,v1 in enumerate(get_travel[ind][f"day{ind+1}"][1].keys()):
                    df_go = itinerary_df_day[itinerary_df_day["step"]== i1+1]
                    name_1 = df_go["name"].values[0]
                    print(name_1)
                    get_travel[ind][f"day{ind+1}"][1][v1]={"name":name_1}
                    get_travel[ind][f"day{ind+1}"][1][v1].update({"lat":float(df_go["lat"].values[0])})
                    get_travel[ind][f"day{ind+1}"][1][v1].update({"lng":float(df_go["lng"].values[0])})

                    if i1 in [0,2,3]: 
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"introduce":concat_df[(concat_df["name"]==name_1) & 
                                                                                (concat_df["source"]=="viewpoint")]["introduce"].values[0]})
                        if get_travel[ind][f"day{ind+1}"][1][v1] == None : get_travel[ind][f"day{ind+1}"][1][v1] = "無"

                    elif i1 in [1,4]: 
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"address":concat_df[(concat_df["name"]==name_1) &
                                                                                (concat_df["source"]=="food")]["address"].values[0]})
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"city":concat_df[(concat_df["name"]==name_1) &
                                                                                (concat_df["source"]=="food")]["city"].values[0]})
                        getstar = concat_df[(concat_df["name"]==name_1) & (concat_df["source"]=="food")]["star"].values[0]
                        if getstar == None: getstar = 0
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"star":getstar})

                        df_gotime=concat_df[(concat_df["name"]==name_1) & (concat_df["source"]=="food")]["time"].values[0].split(",")
                        df_gotime1=[]
                        for _,v in enumerate(df_gotime):
                            v = v.replace('\"',"").replace('\"',"").replace(" ","").strip("[").strip("]")
                            df_gotime1.append(v)   
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"time":df_gotime1})

                    else: 
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"city":concat_df[(concat_df["name"]==name_1) & 
                                                                            (concat_df["source"]=="hotel")]["city"].values[0]})
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"address":concat_df[(concat_df["name"]==name_1) & 
                                                                                (concat_df["source"]=="hotel")]["address"].values[0]})
                        get_travel[ind][f"day{ind+1}"][1][v1].update({"phone":concat_df[(concat_df["name"]==name_1) &
                                                                                (concat_df["source"]=="hotel")]["phone"].values[0]})

                    

            response = jsonify({"message": get_travel, "state": 2})
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response
                
        # except(ValueError) as e:
        #     app.logger.error("Caught exception in post() function:", exc_info=True)
        #     error_message = str(e)
        #     index_of_error = error_message.find(''' (0x27) at index ''')
        #     return jsonify({"message": f"Caught ValueError: {error_message} at index {index_of_error}", "state": 0})
        except(KeyError) as e:
            return jsonify({"message":f"缺少必要的參數: {e}","state":0})
        # except(Exception) as e:
        #     return jsonify({"message":f"due to error: {e}","state":0})
