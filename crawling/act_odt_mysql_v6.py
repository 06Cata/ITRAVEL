import pandas as pd
from datetime import datetime
import pymysql
import wget
import pandas as pd
import re

url = 'https://media.taiwan.net.tw/XMLReleaseALL_public/Activity_C_f.csv'
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
               CREATE TABLE IF NOT EXISTS opendata_act_test
               (id INT AUTO_INCREMENT PRIMARY KEY,
               city_district VARCHAR(100) ,
               activity_name VARCHAR(100) ,
               start_time DATETIME ,
               end_time DATETIME ,
               address VARCHAR(100) ,
               city VARCHAR(100) ,
               district VARCHAR(100),
               activity_lat FLOAT ,
               activity_lng FLOAT ,
               activity_url VARCHAR(255) ,
               photo_url VARCHAR(255)) 
               """)
cursor.execute("SHOW TABLES")


# Define the SQL statement
sql = "INSERT INTO opendata_act_test (city_district,activity_name,start_time,end_time,address,city,district,activity_lat,activity_lng,activity_url,photo_url) VALUES (%s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s)"

# Read the CSV file
data = pd.read_csv('Activity_C_f.csv')


# 1. Merge 'Region' and 'Town' columns and rename it to 'district'
# 2. Rename 'Name' column to 'activity_name'
# 3. Rename 'Px' and 'Py' columns to 'activity_lng' and 'activity_lat'
# 4. Rename 'Picture1' column to 'photo_url'
df = pd.DataFrame(data)
df = df.assign(district=df['Region'] + df['Town'])
df = df.assign(activity_name=df['Name'])
df = df.assign(activity_lng=df['Px'])
df = df.assign(activity_lat=df['Py'])
df = df.assign(photo_url=df['Picture1'])
df = df.assign(address=df['Add'])
df['activity_url'] = None
# Split city and district
df['city_district'] = df['district']
df['city'] = df['district'].str[:3]
df['district'] = df['district'].str[3:]

df = df.where(pd.notnull(df), None)

# Define a function to convert the date string format
def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

# Apply the function to the 'Start' and 'End' columns using the apply method
df['Start'] = df['Start'].apply(convert_date)
df['End'] = df['End'].apply(convert_date)
df = df.assign(start_time=df['Start'])
df = df.assign(end_time=df['End'])

for index, row in df.iterrows():
    # Get data from each row
    city_district = row['city_district']
    activity_name = row['activity_name'] if pd.notnull(row['activity_name']) else None
    start_time = row['start_time'] if pd.notnull(row['start_time']) else None
    end_time = row['end_time'] if pd.notnull(row['end_time']) else None
    address = row['address'] if pd.notnull(row['address']) else None
    city = row['city'] if pd.notnull(row['city']) else None
    district = row['district'] if pd.notnull(row['district']) else None
    activity_lng = row['activity_lng'] if pd.notnull(row['activity_lng']) else None
    activity_lat = row['activity_lat'] if pd.notnull(row['activity_lat']) else None
    activity_url = row['activity_url'] if pd.notnull(row['activity_url']) else None
    photo_url = row['photo_url'] if pd.notnull(row['photo_url']) else None

    # If city_district is blank, extract city and district from the address
    if city_district is None or city_district.strip() == '':
        pattern = r'(.+?(?:區|鎮|市|鄉))'  # Regular expression to match any character until encountering '區', '鎮', or '市'
        if address is not None and '縣' in address and '市' in address:
            modified_address = re.findall(pattern, address)[-1]  # Match the last occurrence that satisfies the regular expression
        elif address is not None:
            match = re.findall(pattern, address)

            if len(match) > 1:
                modified_address = match[0] + match[1]
            elif match:
                modified_address = match[0]
            else:
                modified_address = address
        else:
            modified_address = None

        city_district = modified_address

    # Execute the insert operation
    cursor.execute(sql, (city_district, activity_name, start_time, end_time, address, city, district, activity_lat,
                         activity_lng, activity_url, photo_url))

# Commit the transaction
conn.commit()

# Close the cursor and database connection
cursor.close()
conn.close()

# Print the first few rows of data to check the result
print(data.head())
