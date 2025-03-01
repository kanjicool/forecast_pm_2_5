import requests, json
from datetime import datetime

# URL ของ API
url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"


response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    raise Exception(f"ไม่สามารถดึงข้อมูลได้: {response.status_code}")

station = data["stations"][0]
aqilast = station["AQILast"]

# ดึงข้อมูลตามฟิลด์ที่ต้องการ
station_id = station["stationID"]
timestamp = f"{aqilast['date']} {aqilast['time']}"  # รวม date และ time
pm_25 = float(aqilast["PM25"]["value"])
pm_10 = float(aqilast["PM10"]["value"])
humidity = None 
temperature = None  

# แสดงผล
print(f"Station: {station_id}")
print(f"Timestamp: {timestamp}")
print(f"PM2.5: {pm_25}")
print(f"PM10: {pm_10}")
print(f"Humidity: {humidity}")
print(f"Temperature: {temperature}")