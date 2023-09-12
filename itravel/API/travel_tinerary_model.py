from marshmallow import Schema, fields


# Schema
class travelPostSchema(Schema):
    county = fields.Str(example="臺北市",required=True)
    dates = fields.Int(example=5,required=True)
    departure_date = fields.Date(example="2023-07-24")
    return_date = fields.Date(example="2023-07-26")
    arrive_time = fields.Time(example="03:12:58")
    transportation = fields.Int(example=1)
    mustplace = fields.Str(example="王品牛排,food")
    hotel_level = fields.Int(example=5)
    food_level = fields.Int(example=5)
    viewpoint_level = fields.Int(example=5)
    viewpoint_other_tag = fields.Str(example="室外")
    food_taste_tag = fields.Str(example="火鍋")
    food_price_tag = fields.Int(example=2)
    food_other_tag = fields.Str(example="親子餐廳")
    hotel_price_tag = fields.Int(example=2000)
    hotel_like_tag = fields.Str(example="民宿")

# Response
class travelPostResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.Dict()

