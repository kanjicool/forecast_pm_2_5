# Forecast pm 2.5
Mini Project use LSTM model by kanjicool
This project utilizes a ConvLSTM1D + Bidirectional LSTM model to forecast PM 2.5 levels for the next week.


# web forecast pm 2.5
Use the Air4Thai API to retrieve historical data from the past 7 days as input for a model. The model will then predict PM 2.5 levels for the next week using an autoregressive approach. The predicted values may have slightly reduced accuracy due to the model's output structure during training, which is defined as Dense. This necessitates the use of this method.


ใช้ API ของ air4thai เป็นข้อมูลย้อนหลัง 7 วันส่งไปเป็น Input เข้า model จากนั้นโมเดลจะทำการทำนายค่า PM 2.5 ในอีก 1 สัปดาห์ข้างหน้า โดยใช้หลักการ Autoregressive (ค่าที่ทำนายได้จะมีความแม่นยำที่ลดลงเล็กน้อยเนื่องจากตัวโครงสร้าง Output ของโมเดลในขั้นตอนการ Train ฉันกำหนดให้เป็น Dense จึงเป็นเหตุผลที่ต้องใช้วิธีนี้)

[![LSTM1.png](https://i.postimg.cc/xqV0HKdj/LSTM1.png)](https://postimg.cc/kRw3PR8L)




# Installation Steps
1. Clone the project from GitHub
Open Terminal or Command Prompt and run the following command:

	    git clone https://github.com/kanjicool/forecast_pm_2_5.git

2. Install Poetry (Dependency Manager for this project)

		pip install poetry

		
3. Install Dependencies using Poetry
Run the following command to install all required libraries and frameworks for this project:

	    poetry install

4. Install Node.js and npm
	**Windows**:
	- Download and install Node.js from [nodejs.org](https://nodejs.org/), then verify the installation:
			
			node -v
			npm -v
	**Linux**:  
	- Run the following command in Terminal:

		    sudo apt install nodejs -y
    **macOS**:  
	- Use Homebrew (if installed) or download from [nodejs.org](https://nodejs.org/):

		    brew install node
 
 5. Install Dependencies for Static Files
Navigate to the `static` folder and install npm packages:
	
		cd forecast_pm_2_5/web/static 
		npm install

6. Run the Project
Open Terminal or Command Prompt and execute:
		
		./scripts/run-web 



# ขั้นตอนการติดตั้ง
1. โคลนโปรเจคจาก GitHub
เปิด Terminal หรือ Command Prompt และรันคำสั่งนี้

	    git clone https://github.com/kanjicool/forecast_pm_2_5.git

2. ติดตั้ง poetry (เป็นตัวจัดการไลบราลีใน Project นี้)

		pip install poetry

		
3. ติดตั้ง Dependencies ด้วย Poetry
รันคำสั่งนี้เพื่อติดตั้งไลบรารีและ framework ที่โปรเจคนี้ใช้

	    poetry install

4. ติดตั้ง Node.js และ npm
	**Windows**:
	- ดาวน์โหลดและติดตั้ง Node.js จาก [nodejs.org](https://nodejs.org/) แล้วตรวจสอบการติดตั้ง:
			
			node -v
			npm -v
	**Linux**:  
	- รันคำสั่งใน Terminal:

		    sudo apt install nodejs -y
    **macOS**:  
	- ใช้ Homebrew (ถ้ามี) หรือดาวน์โหลดจาก [nodejs.org](https://nodejs.org/):

		    brew install node
 
 5. ติดตั้ง Dependencies สำหรับ Static Files
 เข้าไปที่โฟลเดอร์ static และติดตั้งแพ็กเกจ npm (ติดตั้ง npm ด้วย) :
	
		cd forecast_pm_2_5/web/static 
		npm install

6. รันโปรเจค
เปิด Terminal หรือ Command Prompt
		
		./scripts/run-web 

