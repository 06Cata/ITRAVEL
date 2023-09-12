import pandas as pd
import numpy as np
from shapely.geometry import Point

# 最高最低平均價格 vs 偏好價格
def calculate_price_score(lower_price, ceiling_price, pref_price ):
    avg_price = (lower_price + ceiling_price)/2
    diff_percent = abs(pref_price - avg_price) / pref_price
    minus_score = diff_percent * 100
    score = (100 - minus_score).apply(lambda x: max(0, x)).astype(int)
    return score


# 價格等級轉換金額 vs 偏好價格
def calculate_price_score_2(price_level, pref_price_level):
    minus_score = (price_level - pref_price_level).apply(lambda x: max(0,x))  # 4-3=1  3-5=0
    score = 100 - minus_score * 20
    return score

# 特徵重疊度
def calculate_tag_score(tag, pref_tag):
    def calculate_score(tags):
        if pd.notna(tags):
            tags_set = set(tags.split(','))  # Convert comma-separated strings to sets
            common = tags_set.intersection(pref_tag)
            return max(20, int(len(common) / len(pref_tag) * 100))
        else:
            return 20
        
    score = tag.apply(calculate_score)
    return score
