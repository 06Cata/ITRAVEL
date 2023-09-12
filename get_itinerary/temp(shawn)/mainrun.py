def mainrun(pref,weekday_name):
    import pandas as pd
    import numpy as np
    # from sqlalchemy import create_engine
    from shapely.geometry import Point
    # from geopy.distance import geodesic
    import warnings
    warnings.filterwarnings("ignore")
    import geopandas as gpd
    from main_function import get_table
    from my_score import calculate_hotel_score, calculate_price_score_3, calculate_tag_score_2

    # 分出群集: 用經緯度 將所有的地點進行分群(clusters)，並畫 map1 以檢視"所有的"clusters分布的狀況。(地圖僅做檢查用 最後要拉掉)
    from sklearn.cluster import DBSCAN
    from sklearn.metrics.pairwise import haversine_distances
    from math import radians
    # import random
    # import folium
    # from folium.plugins import MarkerCluster

    # 傳入資料
    pref = pref

    # 資料庫
    food_select = f"select * from rest_tag_v02 where city = '{pref['county']}'"
    hotel_select = f"select * from hotel_open_data_v3 where city = '{pref['county']}'"
    viewpoint_select = f"select * from okgo_tw_v3 where city = '{pref['county']}'"

    df_viewpoint = get_table(viewpoint_select)
    df_viewpoint = gpd.GeoDataFrame(df_viewpoint, crs="EPSG:4326", geometry=[Point(lnglat) for lnglat in zip(df_viewpoint['lng'], df_viewpoint['lat'])])

    df_food = get_table(food_select)
    df_food = gpd.GeoDataFrame(df_food, crs="EPSG:4326", geometry=[Point(lnglat) for lnglat in zip(df_food['lng'], df_food['lat'])])

    df_hotel = get_table(hotel_select)
    df_hotel = gpd.GeoDataFrame(df_hotel, crs="EPSG:4326", geometry=[Point(lnglat) for lnglat in zip(df_hotel['lng'], df_hotel['lat'])])

    # 給Hotel分數
    df_hotel['like_score'] = calculate_tag_score_2(df_hotel['keyword'], pref["hotel_like_tag"])
    df_hotel['price_score'] = calculate_hotel_score(df_hotel['lower_price'], df_hotel['ceiling_price'], pref['hotel_price_tag'])
    df_hotel['other_score'] = calculate_tag_score_2(df_hotel['tag'], pref["hotel_other_tag"])

    # 計算Hotel加權平均分數 
    # weights = pd.Series([0.4, 0.3, 0.3])
    # df_hotel['overall_score'] = np.average(df_hotel[['like_score', 'price_score', 'other_score']], axis=1, weights=weights)

    # 給Food分數
    df_food['taste_score'] = calculate_tag_score_2(df_food['tag'], pref["food_taste_tag"])
    df_food['price_score'] = calculate_price_score_3(df_food['price_level'], pref['food_price_tag'])
    df_food['other_score'] = calculate_tag_score_2(df_food['tag2'], pref["food_other_tag"]) + 10

    # 計算Food加權平均分數 
    # weights = pd.Series([0.4, 0.3, 0.3])
    # df_food['overall_score'] = np.average(df_food[['taste_score', 'price_score', 'other_score']], axis=1, weights=weights)

    # 給ViewPoint分數
    df_viewpoint['other_score'] = 100
    df_viewpoint['transportation_score'] = 100

    # 計算ViewPoint加權平均分數 
    # weights = pd.Series([0.4, 0.6])
    # df_viewpoint['overall_score'] = np.average(df_viewpoint[['other_score', 'transportation_score']], axis=1, weights=weights)

    # concat 三張表 for next step
    df_food['source']='food'
    df_viewpoint['source']='viewpoint'
    df_hotel['source']='hotel'
    concat_df = pd.concat([df_food, df_viewpoint, df_hotel])
    print(concat_df.shape)

    geo_df = concat_df

    # 将经纬度转换为弧度
    geo_df['lat_rad'] = geo_df['lat'].apply(radians)
    geo_df['lng_rad'] = geo_df['lng'].apply(radians)

    # 计算距离矩阵
    haversine_matrix = haversine_distances(
        geo_df[['lat_rad', 'lng_rad']].values,
        geo_df[['lat_rad', 'lng_rad']].values
    ) * 6371000.0  # 6371000.0 is Earth's radius in meters

    # 运行DBSCAN进行聚类
    dbscan = DBSCAN(eps=2000, min_samples=3, metric='precomputed')
    geo_df['cluster'] = dbscan.fit_predict(haversine_matrix)

    # 分析聚类结果
    num_clusters = len(set(geo_df['cluster'])) - (1 if -1 in geo_df['cluster'] else 0)
    # print(f"Number of clusters: {num_clusters}")
    
    # 创建地图1：显示所有地点的地图
    # m1 = folium.Map(location=[geo_df['lat'].mean(), geo_df['lng'].mean()], zoom_start=12)

    # # 添加 MarkerCluster 层
    # marker_cluster1 = MarkerCluster().add_to(m1)

    # # 在地图上添加地点
    # for _, row in geo_df.iterrows():
    #     folium.Marker(
    #         location=[row['lat'], row['lng']],
    #         popup=row['name'],
    #         icon=None  # 使用默认图标
    #     ).add_to(marker_cluster1)

    # # 保存地图1为HTML文件 (或者 display)
    # m1.save("map1_all_clusters.html")
    # # display(m1)

    # 挑選群集: 旅遊天數N天則挑最大的 N 個 clusters，並畫 map2 以檢視"所挑選的"clusters分布的狀況。(地圖僅做檢查用 最後要拉掉)
    cluster_sizes = geo_df['cluster'].value_counts()

    # 打印所有群集的大小和信息
    print("Cluster Sizes and Information:")
    for cluster_id, size in cluster_sizes.items():
        cluster_points = geo_df[geo_df['cluster'] == cluster_id]
        avg_score = cluster_points['overall_score'].mean()
        
        print(f"Cluster {cluster_id}:")
        print(f" - Size: {size} points")
        print(f" - Average Overall Score: {avg_score:.2f}")
        print(f" - Points:")
        for _, row in cluster_points.iterrows():
            print(f"   - {row['name']} (Lat: {row['lat']}, Lng: {row['lng']}, Overall Score: {row['overall_score']})")
        print("")
        # input("wait")
        
        
    # 找出最大的 N 个群集 (N 用旅遊天數決定)
    n = pref['dates']
    cluster_sizes = geo_df['cluster'].value_counts()
    largest_clusters = cluster_sizes.nlargest(n).index


    # 创建地图2：显示最大3个群集的地点
    # m2 = folium.Map(location=[geo_df['lat'].mean(), geo_df['lng'].mean()], zoom_start=12)

    # 添加 MarkerCluster 层
    # marker_cluster2 = MarkerCluster().add_to(m2)

    # 在地图上添加最大3个群集的地点
    # for cluster_id in largest_clusters:
    #     cluster_points = geo_df[geo_df['cluster'] == cluster_id]
    #     for idx, row in cluster_points.iterrows():
    #         folium.Marker(
    #             location=[row['lat'], row['lng']],
    #             popup=row['name'],
    #             icon=None  # 使用默认图标
    #         ).add_to(marker_cluster2)

    # # 保存地图2为HTML文件 (或者 display)
    # m2.save("map2.html")
    # display(m2)

    # 创建地图
    # m3 = folium.Map(location=[geo_df['lat'].mean(), geo_df['lng'].mean()], zoom_start=12)

    # 设置不同的颜色，用于不同天的行程
    colors = ['red', 'blue', 'green']

    # 初始化每天的行程
    daily_itineraries = []

    # 初始化一个 DataFrame 以存储选定的行程
    selected_itinerary_df = pd.DataFrame(columns=['day', 'step', 'source', 'name', 'lat', 'lng', 'distance']) # distance (跟上一步的距離)

    # 根据聚类拆分数据
    cluster_sizes = geo_df['cluster'].value_counts()
    largest_clusters = cluster_sizes.nlargest(pref['dates']).index
    print(largest_clusters)

    # 检查群集的数量
    while len(largest_clusters) < n:
        # 将所有天数都分配到最大的群集中
        largest_clusters = largest_clusters.insert(0,largest_clusters[0])
        print(largest_clusters)
    

    #取得休息時間的dataframe以及營業時間的dataframe
    if weekday_name != 0:
        restday_select = f"select * from food_rest_day_0802"
        df_restday = get_table(restday_select)
        print(df_restday.shape)

        opentime_select = f"select * from food_rest_interval"
        df_opentime = get_table(opentime_select)
        print(df_opentime.shape)

    # 备份前一个群集的数据，新增欄位use
    prev_cluster_data = None
    geo_df["use"] = 0
    daily_prev_cluster_data = []

    # 遍历每个聚类
    for day, cluster_id in enumerate(largest_clusters):      
        # cluster_color = colors[day % len(colors)]
        cluster_data = geo_df[(geo_df['cluster'] == cluster_id) & (geo_df["use"] == 0)]
        print(f"times {day} cluster_data :" ,cluster_data.shape )

        #找出當天不是休息日的餐廳資料
        if weekday_name != 0 : 
            get_restday = df_restday[df_restday[weekday_name[day]] != "Closed"]
            print(f"times {day} get_restday :" ,get_restday.shape )

            get_opentime = df_opentime[df_opentime['name'].isin(get_restday['name'])]
            print(f"times {day} get_opentime :" ,get_opentime.shape )

        if (prev_cluster_data is not None) and ((cluster_data[cluster_data["source"] == 'viewpoint'].shape[0] < 9 ) or \
            (cluster_data[cluster_data["source"] == 'food'].shape[0] < 12 ) or \
            (cluster_data[cluster_data["source"] == 'hotel'].shape[0] < 3 )): 
            day_1 = day
            while True:
            # 使用前一个群集的数据填充当前的行程
                if day_1 == 0:
                    prev_cluster_data = largest_clusters[0]
                    cluster_data = geo_df[(geo_df['cluster'] == prev_cluster_data) & (geo_df["use"] == 0)]
                    break
                day_1-=1
                prev_cluster_data = largest_clusters[day_1]
                cluster_data = geo_df[(geo_df['cluster'] == prev_cluster_data) & (geo_df["use"] == 0)]
                if (cluster_data[cluster_data["source"] == 'viewpoint'].shape[0] > 9 ) and \
                    (cluster_data[cluster_data["source"] == 'food'].shape[0] > 12 ) and \
                    (cluster_data[cluster_data["source"] == 'hotel'].shape[0] > 3 ): break
            print(f"times {day} final prev_cluster_data :",prev_cluster_data)

        else:
            prev_cluster_data = cluster_id
            print(f"times {day} final prev_cluster_data :",prev_cluster_data)
        
        print(f"times {day} the cluster_data total viewpoint :",cluster_data[cluster_data["source"] == 'viewpoint'].shape)
        print(f"times {day} the cluster_data total food :",cluster_data[cluster_data["source"] == 'food'].shape)   
        print(f"times {day} the cluster_data total hotel :",cluster_data[cluster_data["source"] == 'hotel'].shape)     
        # 存储每天的行程点和信息
        daily_points = []
        daily_info = []

        
        # 挑選viewpoint1
        viewpoint1 = cluster_data[cluster_data['source'] == 'viewpoint'].nlargest(1, 'overall_score').iloc[0]
        daily_points.append(viewpoint1)
        daily_info.append(f"Source: {viewpoint1['source']}, Distance: 0 meters")
        
        getname = viewpoint1["name"]
        geo_df.loc[geo_df["name"]==getname,"use"] = 1
        print(f"times {day} viewpoint1 :" ,viewpoint1.shape )
        
        # 挑選food1
        distance_threshold = 500

        #找出中午有營業的餐廳資料
        if weekday_name != 0 : 
            food1_opentime = get_opentime[get_opentime[f'{weekday_name[day]}_lunch'] != 0 ]

            food1 = cluster_data[(cluster_data['source'] == 'food') & (cluster_data['name'].isin(food1_opentime['name'])) &
                            (cluster_data.geometry.distance(viewpoint1.geometry)*111.32*1000 <= distance_threshold)]
            print(f"times {day} food1-1 :" ,food1.shape )
            
            while len(food1) < 1:
                distance_threshold += 100
                food1 = cluster_data[(cluster_data['source'] == 'food') & (cluster_data['name'].isin(food1_opentime['name'])) &
                            (cluster_data.geometry.distance(viewpoint1.geometry)*111.32*1000 <= distance_threshold)]
                print(f"times {day} food1-2 :" ,food1.shape )
        else : 
            food1 = cluster_data[(cluster_data['source'] == 'food') &
                        (cluster_data.geometry.distance(viewpoint1.geometry)*111.32*1000 <= distance_threshold)]
            print(f"times {day} food1-1-1 :" ,food1.shape )
            
            while len(food1) < 1:
                distance_threshold += 100
                food1 = cluster_data[(cluster_data['source'] == 'food') & 
                            (cluster_data.geometry.distance(viewpoint1.geometry)*111.32*1000 <= distance_threshold)]
                print(f"times {day} food1-2-2 :" ,food1.shape )
        
        food1 = food1.nlargest(1, 'overall_score').iloc[0]
        daily_points.append(food1)
        distance_to_previous = food1.geometry.distance(viewpoint1.geometry)*111.32*1000
        daily_info.append(f"Source: {food1['source']}, Distance: {distance_to_previous:.2f} meters")

        getname = food1["name"]
        geo_df.loc[geo_df["name"]==getname,"use"] = 1
        print(f"times {day} food1 :" ,food1.shape )

        # 挑選viewpoint2
        distance_threshold = 600
        viewpoint2 = cluster_data[(cluster_data['source'] == 'viewpoint') &
                                (cluster_data.geometry.distance(food1.geometry)*111.32*1000 <= distance_threshold) &
                                (cluster_data['id'] != viewpoint1['id'])]
        print(f"times {day} viewpoint2-1 :" ,viewpoint2.shape )
        
        while len(viewpoint2) < 1:
            distance_threshold += 100
            viewpoint2 = cluster_data[(cluster_data['source'] == 'viewpoint') &
                            (cluster_data.geometry.distance(viewpoint1.geometry)*111.32*1000 <= distance_threshold) &
                            (cluster_data['id'] != viewpoint1['id'])]
            print(f"times {day} viewpoint2-2 :" ,viewpoint2.shape )
                   
        viewpoint2 = viewpoint2.nlargest(1, 'overall_score').iloc[0]  
        print(f"times {day} viewpoint2-id :",viewpoint2["id"])     
        daily_points.append(viewpoint2)
        distance_to_previous = viewpoint2.geometry.distance(food1.geometry)*111.32*1000
        daily_info.append(f"Source: {viewpoint2['source']}, Distance: {distance_to_previous:.2f} meters")

        getname = viewpoint2["name"]
        geo_df.loc[geo_df["name"]==getname,"use"] = 1
        print(f"times {day} viewpoint2 :" ,viewpoint2.shape )

        # 挑選viewpoint3
        distance_threshold = 700
        viewpoint3 = cluster_data[(cluster_data['source'] == 'viewpoint') &
                                (cluster_data.geometry.distance(viewpoint2.geometry)*111.32*1000 <= distance_threshold) &
                                (cluster_data['id'] != viewpoint1['id']) &
                                (cluster_data['id'] != viewpoint2['id'])]
        print(f"times {day} viewpoint3-1 :" ,viewpoint3.shape )
        
        while len(viewpoint3) < 1:
            distance_threshold += 100
            viewpoint3 = cluster_data[(cluster_data['source'] == 'viewpoint') &
                            (cluster_data.geometry.distance(viewpoint2.geometry)*111.32*1000 <= distance_threshold) &
                            (cluster_data['id'] != viewpoint1['id']) &
                            (cluster_data['id'] != viewpoint2['id'])]
            print(f"times {day} viewpoint3-2 :" ,viewpoint3["id"] )
            
        
        viewpoint3 = viewpoint3.nlargest(1, 'overall_score').iloc[0]
        daily_points.append(viewpoint3)
        distance_to_previous = viewpoint3.geometry.distance(viewpoint2.geometry)*111.32*1000
        daily_info.append(f"Source: {viewpoint3['source']}, Distance: {distance_to_previous:.2f} meters")

        getname = viewpoint3["name"]
        geo_df.loc[geo_df["name"]==getname,"use"] = 1
        print(f"times {day} viewpoint3-3 :" ,viewpoint3.shape )
        # 挑選food2
        distance_threshold = 500

        #找出晚上有營業的餐廳資料
        if weekday_name != 0 : 
            food2_opentime = get_opentime[get_opentime[f'{weekday_name[day]}_dinner'] != 0 ]

            food2 = cluster_data[(cluster_data['source'] == 'food') & (cluster_data['name'].isin(food2_opentime['name'])) &
                            (cluster_data.geometry.distance(viewpoint3.geometry)*111.32*1000 <= distance_threshold) &
                            (cluster_data['id'] != food1['id'])]
            
            while len(food2) < 1:
                distance_threshold += 100
                food2 = cluster_data[(cluster_data['source'] == 'food') & (cluster_data['name'].isin(food2_opentime['name'])) &
                            (cluster_data.geometry.distance(viewpoint3.geometry)*111.32*1000 <= distance_threshold) &
                            (cluster_data['id'] != food1['id'])]
        else : 
            food2 = cluster_data[(cluster_data['source'] == 'food') &
                        (cluster_data.geometry.distance(viewpoint3.geometry)*111.32*1000 <= distance_threshold) &
                        (cluster_data['id'] != food1['id'])]
            
            while len(food2) < 1:
                distance_threshold += 100
                food2 = cluster_data[(cluster_data['source'] == 'food') & 
                            (cluster_data.geometry.distance(viewpoint3.geometry)*111.32*1000 <= distance_threshold) &
                            (cluster_data['id'] != food1['id'])]
        
        food2 = food2.nlargest(1, 'overall_score').iloc[0]
        daily_points.append(food2)
        distance_to_previous = food2.geometry.distance(viewpoint3.geometry)*111.32*1000
        daily_info.append(f"Source: {food2['source']}, Distance: {distance_to_previous:.2f} meters")

        getname = food2["name"]
        geo_df.loc[geo_df["name"]==getname,"use"] = 1
        print(f"times {day} food2 :" ,food2.shape )
        # 挑選hotel
        if (day != 0) and (cluster_id == largest_clusters[day-1] or cluster_id != prev_cluster_data):
            if prev_cluster_data in daily_prev_cluster_data:
                index_1 = daily_prev_cluster_data.index(prev_cluster_data)
            else: 
                index_1 = list(largest_clusters).index(prev_cluster_data)
            hotel = daily_itineraries[index_1][0][5]
            daily_points.append(hotel)
        else:
            distance_threshold = 600
            hotel = cluster_data[(cluster_data['source'] == 'hotel') &
                                (cluster_data.geometry.distance(viewpoint3.geometry)*111.32*1000 <= distance_threshold)]
            while len(hotel) < 1:
                distance_threshold += 100
                hotel = cluster_data[(cluster_data['source'] == 'hotel') &
                                    (cluster_data.geometry.distance(viewpoint3.geometry)*111.32*1000 <= distance_threshold)]
            hotel = hotel.nlargest(1, 'overall_score').iloc[0]
            daily_points.append(hotel)
        distance_to_previous = hotel.geometry.distance(viewpoint3.geometry)*111.32*1000
        daily_info.append(f"Source: {hotel['source']}, Distance: {distance_to_previous:.2f} meters")

        getname = hotel["name"]
        geo_df.loc[geo_df["name"]==getname,"use"] = 1
        print(f"times {day} hotel :" ,hotel.shape )
        # 将每天的行程点存入每天的行程表中
        if (prev_cluster_data != cluster_id) and (prev_cluster_data in daily_prev_cluster_data):
            index_1 = list(largest_clusters).index(prev_cluster_data)
            daily_itineraries.insert(daily_prev_cluster_data.index(prev_cluster_data)+1,(daily_points, daily_info))
            daily_prev_cluster_data.insert(daily_prev_cluster_data.index(prev_cluster_data)+1,prev_cluster_data)
            print("insert daily itineraries")
            print("daily_prev_cluster_data is :",daily_prev_cluster_data)

        else:    
            daily_itineraries.append((daily_points, daily_info))
            daily_prev_cluster_data.append(prev_cluster_data)
            print("append daily itineraries")
            print("daily_prev_cluster_data is :",daily_prev_cluster_data)

        
    # 将每天的行程信息添加到 DataFrame
    for i1 , v1 in enumerate(daily_itineraries):
        step = 1
        for point, info in zip(v1[0], v1[1]):
            selected_itinerary_df = pd.concat([selected_itinerary_df, pd.DataFrame([{'day': i1 + 1,
                                                                'name': point['name'],
                                                                'lat': point['lat'],
                                                                'lng': point['lng'],
                                                                'source': point['source'],
                                                                'distance': info.split(": ")[-1],
                                                                'step': step}])], ignore_index=True)

            step += 1
        
        # 在地图上标示每天的行程点
    #     marker_cluster = MarkerCluster().add_to(m3)
    #     for point, info in zip(daily_points, daily_info):
    #         folium.Marker(
    #             location=[point['lat'], point['lng']],
    #             popup=f"{point['name']} - {info}",
    #             icon=folium.Icon(color=cluster_color)
    #         ).add_to(marker_cluster)

    # # 保存地图为HTML文件 (或者 display)
    # m3.save("map3.html")
    # display(m3)

    # 輸出行程: 以 df 丟回去給 Lewis的API (或要在這邊轉好JSON也行)
    # Output DataFrame:
    return selected_itinerary_df,concat_df
