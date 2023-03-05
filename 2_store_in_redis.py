import redis
import pandas as pd

r = redis.Redis(host='localhost', port=6379, db=0)

df = pd.read_csv('./data.csv')
df_sorted = df.sort_values(by='sts')

for _, row in df_sorted.iterrows():
    device_id = row['device_fk_id']
    data = {
        'latitude': row['latitude'],
        'longitude': row['longitude'],
        'time_stamp': row['time_stamp'],
        'sts': row['sts'],
        'speed':row['speed']
    }
    r.hset(device_id, mapping=data)

print("Done!!!")