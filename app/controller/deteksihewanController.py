from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

# Memuat model yang sudah dilatih
try:
    model = load_model('deteksi_hewan_model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

router = APIRouter()

@router.post("/deteksihewan")
async def deteksi_hewan(file: UploadFile = File(...)):
    # Validasi jika model tidak berhasil dimuat
    if model is None:
        return JSONResponse(status_code=500, content={"error": "Model failed to load"})

    try:
        # Membaca file gambar
        img_data = await file.read()
        img = Image.open(BytesIO(img_data))
        
        # Pastikan gambar dalam format RGB
        img = img.convert("RGB")
        
        # Mengubah ukuran gambar sesuai dengan pelatihan model
        img = img.resize((150, 150))
        
        # Normalisasi gambar
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Tambahkan dimensi batch
        
        # Melakukan prediksi menggunakan model
        prediction = model.predict(img_array)
        
        # Menentukan hasil berdasarkan prediksi
        result = "kucing" if prediction[0][0] > 0.5 else "ayam"
        
        return JSONResponse(content={"prediction": result})
    
    except Exception as e:
        # Tangkap error yang terjadi selama pemrosesan gambar atau prediksi
        return JSONResponse(status_code=400, content={"error": f"Error during image processing or prediction: {str(e)}"})
