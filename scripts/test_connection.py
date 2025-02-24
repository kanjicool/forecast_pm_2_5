import mongoengine as me
from mongoengine import connection

MONGODB_DB = "forecast_pm_2_5db"
me.connect(MONGODB_DB, host="localhost", port=27017)

# ตรวจสอบข้อมูลการเชื่อมต่อ
print(connection.get_connection().server_info())
