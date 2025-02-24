from forecast_pm_2_5 import models
import mongoengine as me

MONGODB_DB = "forecast_pm_2_5db"
me.connect(MONGODB_DB, host="localhost", port=27017)

def init_admin():
    if models.User.objects(username="admin").first():
        print("already have admin user in database")
        return
    admin_user = models.User(
        first_name="Admin",  # กรอกข้อมูลฟิลด์ first_name
        last_name="User",    # กรอกข้อมูลฟิลด์ last_name
        username="admin", 
        password="admin123", 
        email="admin@example.com",  # กรอกข้อมูลฟิลด์ email
        roles=["admin"]
    )
    admin_user.set_password("admin123")
    admin_user.save()
    print("Admin user created")

# เรียกใช้ฟังก์ชันนี้เมื่อรันไฟล์
init_admin()
