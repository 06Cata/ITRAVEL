# import pandas as pd
# from shapely.geometry import Point
# import numpy as np
# # # 最高最低平均價格 vs 偏好價格
# # # def calculate_price_score(lower_price, ceiling_price, pref_price ):
# # #     avg_price = (lower_price + ceiling_price)/2
# # #     print("pref_price:", pref_price)
# # #     print("avg_price:", avg_price)

# # #     if pref_price == 0 : diff_percent = avg_price
# # #     else: diff_percent = abs(pref_price - avg_price) / pref_price
# # #     minus_score = diff_percent * 100.0
# # #     score = (100.0 - minus_score).apply(lambda x: max(0, x)).astype(int)
# # #     return score


# # def calculate_price_score(lower_price, ceiling_price, pref_price):
# #     pref_price = float(pref_price)

# #     avg_price = (lower_price + ceiling_price) / 2
    
# #     diff_percent = np.abs(pref_price - avg_price) / pref_price
# #     minus_score = diff_percent * 100
# #     score = (100 - minus_score).apply(lambda x: max(0, x)).astype(int)
# #     return score


# # # 價格等級轉換金額 vs 偏好價格
# # def calculate_price_score_2(price_level, pref_price_level):
# #     minus_score = (price_level - pref_price_level).apply(lambda x: max(0,x))  # 4-3=1  3-5=0
# #     score = 100.0 - minus_score * 20
# #     return score

# # # 特徵重疊度
# # def calculate_tag_score(tag, pref_tag):
# #     def calculate_score(tags):
# #         if pd.notna(tags) and len(pref_tag)!=0:
# #             tags_set = set(tags.split(','))  # Convert comma-separated strings to sets
# #             common = tags_set.intersection(pref_tag)
# #             return max(20, int(len(common) / len(pref_tag) * 100.0))
# #         else:
# #             return 20
        
# #     score = tag.apply(calculate_score)
# #     return score

# import numpy as np

# def calculate_price_score(lower_price, ceiling_price, pref_price):
#     pref_price = float(pref_price)
#     avg_price = (lower_price + ceiling_price) / 2
#     diff_percent = np.abs(pref_price - avg_price) / pref_price

#     # 檢查是否有非有限值（NA或inf）
#     if not np.isfinite(diff_percent):
#         # 處理方式：假設缺失值為最大分數
#         diff_percent = 1.0

#     minus_score = diff_percent * 100
#     score = pd.Series(100 - minus_score).apply(lambda x: max(0, x)).astype(int)
#     return score

# def calculate_price_score_2(price_level, pref_price_level):
#     price_level = pd.Series(price_level, dtype=float)
#     pref_price_level = pd.Series(pref_price_level, dtype=float)
#     minus_score = (price_level - pref_price_level).apply(lambda x: max(0, x))  # 4-3=1  3-5=0

#     # 檢查是否有非有限值（NA或inf）
#     if not np.isfinite(minus_score).all():
#         # 處理方式：假設缺失值為最大分數
#         minus_score = 1.0

#     score = 100.0 - minus_score * 20
#     return score

# def calculate_tag_score(tag, pref_tag):
#     def calculate_score(tags):
#         if pd.notna(tags) and len(pref_tag) != 0:
#             tags = str(tags)  # Ensure tags are converted to string
#             tags_set = set(tags.split(','))  # Convert comma-separated strings to sets
#             common = tags_set.intersection(pref_tag)
#             return max(20, int(len(common) / len(pref_tag) * 100.0))
#         else:
#             return 20

#     tag = pd.Series(tag, dtype=str)  # Convert to string dtype

#     # 檢查是否有非有限值（NA或inf）
#     if not np.isfinite(tag):
#         # 處理方式：假設缺失值為最小分數
#         tag = 0

#     score = tag.apply(calculate_score)
#     return score
import pandas as pd
from shapely.geometry import Point
import numpy as np

def calculate_price_score(lower_price, ceiling_price, pref_price):
    pref_price = float(pref_price)
    avg_price = (lower_price + ceiling_price) / 2
    diff_percent = np.abs(pref_price - avg_price) / pref_price

    minus_score = diff_percent * 100
    score = (100 - minus_score).apply(lambda x: max(0, x)).astype(int)
    return score

def calculate_price_score_2(price_level, pref_price_level):
    price_level = price_level.astype(float)
    pref_price_level = pd.Series(pref_price_level)

    pref_price_level = pref_price_level.astype(float)
    minus_score = (price_level - pref_price_level).apply(lambda x: max(0, x))

    score = 100.0 - minus_score * 20
    return score

def calculate_tag_score(tag, pref_tag):
    def calculate_score(tags):
        if pd.notna(tags) and len(pref_tag) != 0:
            tags = str(tags)
            tags_set = set(tags.split(','))
            common = tags_set.intersection(pref_tag)
            return max(20, int(len(common) / len(pref_tag) * 100.0))
        else:
            return 20

    tag = tag.astype(str)
    score = tag.apply(calculate_score)
    return score


