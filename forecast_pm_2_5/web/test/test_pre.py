import requests
import numpy as np

url = "http://127.0.0.1:8080/predict"

# ข้อมูลล่าสุดที่มี
latest_features = [35, 25, 60, 20]

# ทำให้เป็น 7 timestamps โดยใช้ค่าซ้ำกัน
features = np.tile(latest_features, (7, 1)).tolist()  # shape (7, 4)

data = {"features": features}

response = requests.post(url, json=data)
print(response.json())
