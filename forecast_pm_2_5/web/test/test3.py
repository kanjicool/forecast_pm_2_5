import requests
from datetime import datetime, timedelta
import json
import numpy as np
from forecast_pm_2_5.models import load_forecast_model

# กำหนดรหัสสถานี
station_id = "02t"
params = "PM25,PM10"

# กำหนดช่วงเวลา (ย้อนไป 7 วัน)
end_datetime = datetime.now() - timedelta(days=1)
start_datetime = end_datetime - timedelta(days=6)
start_date_str = start_datetime.strftime("%Y-%m-%d")
end_date_str = end_datetime.strftime("%Y-%m-%d")
start_hour = 0
end_hour = 23

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
    except requests.exceptions.JSONDecodeError as e:
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

# ดึงข้อมูลจาก "stations"[0]["data"]
if isinstance(data, dict) and "stations" in data:
    station_data = data["stations"][0]["data"]
    if isinstance(station_data, list):
        # เก็บข้อมูลตามวัน
        daily_data = {}
        for entry in station_data:
            timestamp = entry.get("DATETIMEDATA", "N/A")
            date = timestamp.split(" ")[0]
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
        for date in sorted(daily_data.keys())[-7:]:
            pm25_avg = np.mean(daily_data[date]["PM25"]) if daily_data[date]["PM25"] else 0
            pm10_avg = np.mean(daily_data[date]["PM10"]) if daily_data[date]["PM10"] else 0
            humidity = 0
            temperature = 0
            features.append([pm25_avg, pm10_avg, humidity, temperature])
            print(f"Date: {date}, PM2.5: {pm25_avg}")

        # โหลดโมเดล
        model = load_forecast_model()
        predictions = []

        # วนลูปทำนาย 7 วันถัดไป
        current_features = features.copy()
        for i in range(7):
            input_data = np.array(current_features[-7:]).reshape(1, 1, 7, 4)
            pred = max(0, model.predict(input_data)[0][0])  # จำกัดไม่ให้ติดลบ
            predictions.append(pred)

            # อัปเดต features ด้วยค่าที่ทำนาย
            new_feature = [pred, 0, 0, 0]
            current_features.append(new_feature)

        # แสดงผลลัพธ์
        print("\nPredicted PM2.5 for next 7 days:")
        for i, pred in enumerate(predictions, 1):
            future_date = (end_datetime + timedelta(days=i)).strftime("%Y-%m-%d")
            print(f"Day {i} ({future_date}): PM2.5 = {pred:.2f}")
else:
    print("Data is not a valid response:", data)