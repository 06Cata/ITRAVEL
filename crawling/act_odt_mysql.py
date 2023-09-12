import pandas as pd
from datetime import datetime
import pymysql
import wget
import pandas as pd
from datetime import datetime
import pymysql

url = '	https://media.taiwan.net.tw/XMLReleaseALL_public/Activity_C_f.csv'
output_file = 'Activity_C_f.csv'
wget.download(url, out=output_file)

conn = pymysql.connect(
    host='127.0.0.1',
    database='travel',
    user='root',
    password='123456',
    port=3306
    )

# Create a cursor object
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS opendata_act
               (id INT AUTO_INCREMENT PRIMARY KEY,
               district VARCHAR(255) ,
               activy_name VARCHAR(255) ,
               start_time DATETIME ,
               end_time DATETIME ,
               address VARCHAR(255) ,
               activy_lng FLOAT ,
               activy_lat FLOAT ,
               activy_url VARCHAR(255) ,
               photo_url VARCHAR(255)) 
               """)
cursor.execute("SHOW TABLES")


# Define the SQL statement
sql = "INSERT INTO opendata_act (district,activy_name,start_time,end_time,address,activy_lng,activy_lat,activy_url,photo_url) VALUES (%s,%s, %s,%s, %s,%s, %s,%s, %s)"

# 讀取CSV文件
data = pd.read_csv('Activity_C_f.csv')

#1.Region’、 ‘Town’這兩欄要合併，欄位名稱叫district
#2.Name欄位要改名叫activy_name
#3.'Px'、'Py'欄位要改名activy_lng、activy_lat
#4.Picture1欄位要改名叫photo_url
df = pd.DataFrame(data)
df = df.assign(district=df['Region'] + df['Town'])
df = df.assign(activy_name=df['Name'])
df = df.assign(activy_lng=df['Px'])
df = df.assign(activy_lat=df['Py'])
df = df.assign(photo_url=df['Picture1'])
df = df.assign(address=df['Add'])
df['activy_url'] = None
df = df.where(pd.notnull(df), None)

# 定義函数来轉換日期字符串格式
def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

# 使用apply方法應用函数到'Start'列
df['Start'] = df['Start'].apply(convert_date)
df['End'] = df['End'].apply(convert_date)
df = df.assign(start_time=df['Start'])
df = df.assign(end_time=df['End'])

for index, row in df.iterrows():
    # 獲取每一行的數據
    district = row['district']
    activy_name = row['activy_name'] if pd.notnull(row['activy_name']) else None
    start_time = row['start_time'] if pd.notnull(row['start_time']) else None
    end_time = row['end_time'] if pd.notnull(row['end_time']) else None
    address = row['address'] if pd.notnull(row['address']) else None
    activy_lng = row['activy_lng'] if pd.notnull(row['activy_lng']) else None
    activy_lat = row['activy_lat'] if pd.notnull(row['activy_lat']) else None
    activy_url = row['activy_url'] if pd.notnull(row['activy_url']) else None
    photo_url = row['photo_url'] if pd.notnull(row['photo_url']) else None

    # 執行插入操作
    cursor.execute(sql, (district, activy_name, start_time, end_time, address, activy_lng, activy_lat, activy_url, photo_url))

# data = (id,district,activy_name,start_time,end_time,address,activy_lng,activy_lat,activy_url,photo_url)

#提交事務
conn.commit()

# 關閉游標和資料庫連接
cursor.close()
conn.close()

# 打印前幾行數據檢查結果
print(data.head())
