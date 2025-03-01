from flask import Blueprint, render_template, jsonify
from datetime import datetime, timedelta
import requests
import json
import numpy as np
from forecast_pm_2_5.models import load_forecast_model

module = Blueprint("site", __name__)
model = load_forecast_model()

@module.route("/")
def index():
    return render_template("/site/index.html")

@module.route("/predict", methods=["GET"])
def predict_pm25():
    try:
        # กำหนดรหัสสถานี
        station_id = "02t"
        params = "PM25,PM10"

        # ใช้วันที่ปัจจุบันจริง ๆ
        today = datetime.now()
        end_datetime = today - timedelta(days=1)  # วันก่อนหน้า
        start_datetime = end_datetime - timedelta(days=6)  # ย้อนหลัง 7 วัน
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

        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch data from API (Status: {response.status_code})", "raw_response": response.text}), 500

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            raw_text = response.text.replace('result:', '"result":').replace('error:', '"error":')
            try:
                data = json.loads(raw_text)
            except json.JSONDecodeError:
                print("Still not valid JSON:", raw_text)
                return jsonify({"error": "API response is not valid JSON", "raw_response": raw_text}), 500

        # ตรวจสอบโครงสร้างข้อมูล
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

                # คำนวณค่าเฉลี่ยรายวันและจัดเป็น features (ย้อนหลัง 7 วัน)
                past_features = []
                past_dates = sorted(daily_data.keys())[-7:]
                for date in past_dates:
                    pm25_avg = np.mean(daily_data[date]["PM25"]) if daily_data[date]["PM25"] else 0
                    pm10_avg = np.mean(daily_data[date]["PM10"]) if daily_data[date]["PM10"] else 0
                    humidity = 0
                    temperature = 0
                    past_features.append([pm25_avg, pm10_avg, humidity, temperature])

                # ทำนาย 7 วันถัดไป
                predictions = []
                current_features = past_features.copy()
                for i in range(7):
                    input_data = np.array(current_features[-7:]).reshape(1, 1, 7, 4)
                    pred = max(0, model.predict(input_data)[0][0])  # จำกัดไม่ให้ติดลบ
                    predictions.append(pred)
                    new_feature = [pred, 0, 0, 0]
                    current_features.append(new_feature)

                # สร้างข้อมูลสำหรับกราฟ
                past_data = [{"date": date, "pm25": float(round(pm25_avg, 2))} for date, pm25_avg in zip(past_dates, [feat[0] for feat in past_features])]
                forecast_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 8)]
                forecast_data = [{"date": date, "pm25": float(round(pred, 2))} for date, pred in zip(forecast_dates, predictions)]

                return jsonify({"past": past_data, "forecast": forecast_data, "today": today.strftime("%Y-%m-%d")})
            else:
                return jsonify({"error": "No data list found in stations", "raw_response": response.text}), 500
        else:
            return jsonify({"error": "Invalid API response structure", "raw_response": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e), "raw_response": response.text if 'response' in locals() else "No response"}), 500