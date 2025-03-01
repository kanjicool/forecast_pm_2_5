import requests
from datetime import datetime, timedelta
import json
import numpy as np

# กำหนดรหัสสถานี
station_id = "02t"
params = "PM25,PM10"

# กำหนดช่วงเวลา (ย้อนไป 7 วัน)
end_datetime = datetime.now() - timedelta(days=1)  # เมื่อวาน
start_datetime = end_datetime - timedelta(days=6)  # ย้อนหลัง 7 วัน (รวมทั้งหมด 7 วัน)
start_date_str = start_datetime.strftime("%Y-%m-%d")
end_date_str = end_datetime.strftime("%Y-%m-%d")
start_hour = 0  # เริ่มต้น 00:00
end_hour = 23   # สิ้นสุด 23:00

# สร้าง URL (แก้ ¶m เป็น param)
url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={params}&type=hr&sdate={start_date_str}&edate={end_date_str}&stime={start_hour}&etime={end_hour}"
print("Generated URL:", url)

# ดึงข้อมูล
response = requests.get(url)
print("Status Code:", response.status_code)
print("Raw Response:", response.text)

if response.status_code == 200:
    try:
        data = response.json()
    except ValueError as e:
        print("JSON Decode Error:", e)
        print("Response is not JSON, attempting manual fix")
        raw_text = response.text.replace('result:', '"result":').replace('error:', '"error":')
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            print("Still not valid JSON:", raw_text)
            data = raw_text
else:
    raise Exception(f"ไม่สามารถดึงข้อมูลได้: {response.status_code}")

# ตรวจสอบประเภทของ data
print("Data Type:", type(data))

# ดึงข้อมูลจาก "stations"[0]["data"]
if isinstance(data, dict) and "stations" in data:
    station_data = data["stations"][0]["data"]
    if isinstance(station_data, list):
        # เก็บข้อมูลตามวัน
        daily_data = {}
        for entry in station_data:
            timestamp = entry.get("DATETIMEDATA", "N/A")
            date = timestamp.split(" ")[0]  # ดึงเฉพาะวันที่
            pm_25 = float(entry["PM25"]) if entry.get("PM25") is not None else None
            pm_10 = float(entry["PM10"]) if entry.get("PM10") is not None else None

            if date not in daily_data:
                daily_data[date] = {"PM25": [], "PM10": []}
            if pm_25 is not None:
                daily_data[date]["PM25"].append(pm_25)
            if pm_10 is not None:
                daily_data[date]["PM10"].append(pm_10)

        # คำนวณค่าเฉลี่ยรายวันและจัดเป็น features
        features = []
        for date in sorted(daily_data.keys())[-7:]:  # เอา 7 วันล่าสุด
            pm25_avg = np.mean(daily_data[date]["PM25"]) if daily_data[date]["PM25"] else 0  # ใช้ 0 ถ้าไม่มีข้อมูล
            pm10_avg = np.mean(daily_data[date]["PM10"]) if daily_data[date]["PM10"] else 0  # ใช้ 0 ถ้าไม่มีข้อมูล
            humidity = 0  # ไม่มีใน API ใช้ 0 เป็น default
            temperature = 0  # ไม่มีใน API ใช้ 0 เป็น default
            features.append([pm25_avg, pm10_avg, humidity, temperature])

            print(f"Date: {date}")
            print(f"Daily PM2.5: {pm25_avg}")
            print(f"Daily PM10: {pm10_avg}")
            print(f"Humidity: {humidity}")
            print(f"Temperature: {temperature}")
            print("---")

        # ปรับ shape ให้เข้ากับ LSTM
        input_data = np.array(features).reshape(1, 7, 4)  # หรือ (1, 1, 7, 4) ตามโมเดล
        print("Input shape for LSTM:", input_data.shape)
        print("Input data for LSTM:", input_data)

    else:
        print("No data list found in stations:", station_data)
elif isinstance(data, dict) and "result" in data:
    print("API Error:", data.get("error", "Unknown error"))
else:
    print("Data is not a valid response:", data)