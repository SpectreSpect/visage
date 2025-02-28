# Visage API

Visage is a FastAPI-based application that generates images using a reference image and a text prompt. The API integrates Midjourney-style image generation with face swapping to retain the reference subject's identity in the generated output.

## 🚀 Features
- Accepts a **reference image** and a **text prompt**
- Generates an image based on the prompt
- Performs **face swapping** to maintain the reference subject's identity
- Returns the final **face-swapped generated image**
- Logs all requests and errors for debugging

## 📦 Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/SpectreSpect/visage.git
cd visage
```

### **2. Set Up a Virtual Environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the root directory and add:
```env
GPTUNNEL_API_KEY=your_gptunnel_api_key
IMGBB_API_KEY=your_imgbb_api_key
DEBUG=True  # Set to False in production
```

## 🚀 Running the API
Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at:
```
http://127.0.0.1:8000
```

## 📖 API Endpoints

### **1. Health Check**
#### **`GET /`**
Checks if the API is running.
```json
{
  "message": "Welcome to the Visage API!"
}
```

---

### **2. Generate Image**
#### **`POST /generate`**
Generates an image based on a **reference image** and a **text prompt**, then performs **face swapping**.

#### **🔹 Request Parameters:**
| Parameter   | Type        | Required | Description |
|------------|------------|----------|-------------|
| `prompt`   | `string`   | ✅ Yes   | Text description of the desired image. |
| `image`    | `file`     | ✅ Yes   | Reference image of the person. |

#### **🔹 Example Request:**
```py
import requests

url = "http://127.0.0.1:8000/generate"
files = {"image": open("image.jpg", "rb")}
data = {"prompt": "A snowy winter landscape with a man in warm clothing."}
response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open("output.png", "wb") as file:
        file.write(response.content)
```

#### **🔹 Example Response:**
- **Success (200 OK)**: Returns the generated **face-swapped image** (`image/png`).
- **Failure (400/500)**: Returns an error message.

## 📂 Logging
- Logs are saved to `logs/app.log`.
- Uploaded images are stored in:
  - `logs/uploads/reference/`
  - `logs/uploads/generated/`
  - `logs/uploads/face_swapped/`
- Errors are logged with detailed stack traces (if `DEBUG=True`).

## 🛠️ Technologies Used
- **FastAPI** (API Framework)
- **PIL (Pillow)** (Image Processing)
- **NumPy** (Array Manipulation)
- **Requests** (API Calls)
- **Uvicorn** (ASGI Server)


## 📜 License
This project is licensed under the **MIT License**.


