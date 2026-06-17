✅ Required Libraries
requirements.txt (GitHub ready — ONE LINE format)
opencv-python numpy

If you want a slightly more stable setup (recommended for students):

opencv-python==4.9.0.80 numpy==1.26.4
🚀 Install in VS Code (One Command)

Run this in terminal:

pip install opencv-python numpy
📦 Optional (if video causes issues)

Sometimes OpenCV needs extra backend support:

pip install opencv-python-headless

(Use this ONLY if GUI window doesn’t open properly)

🗂️ Recommended Project Structure
Parking-Lot-Detection/
│
├── main.py
├── car_park_7_lots.mp4
├── requirements.txt
├── README.md
└── .gitignore
🧠 Quick VS Code Setup Steps
Open VS Code
Open folder
Open terminal
Run:
python -m venv venv
venv\Scripts\activate   # Windows
Install dependencies:
pip install -r requirements.txt
Run project:
python main.py
⚠️ Important Note for Students

Make sure video file name matches exactly:

car_park_7_lots.mp4
If video doesn't load → check path or put video in same folder as main.py
