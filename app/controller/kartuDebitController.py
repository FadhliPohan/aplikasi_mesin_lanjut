from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

# Membuat router untuk aplikasi
router = APIRouter()

# Model Pydantic untuk menerima input
class CreditCardApplication(BaseModel):
    nama: str
    umur: int
    pekerjaan: str
    penghasilan: int
    alamat: str

# Data pelatihan contoh (umumkan/anggarakan bahwa pekerjaan sudah terklasifikasi)
data_latihan = [
    {'umur': 30, 'pekerjaan': 'Karyawan', 'penghasilan': 5000000, 'status': 'Disetujui'},
    {'umur': 22, 'pekerjaan': 'Freelancer', 'penghasilan': 2000000, 'status': 'Tidak Disetujui'},
    {'umur': 35, 'pekerjaan': 'Pegawai Negeri', 'penghasilan': 8000000, 'status': 'Disetujui'},
    {'umur': 28, 'pekerjaan': 'Freelancer', 'penghasilan': 3000000, 'status': 'Tidak Disetujui'},
    {'umur': 40, 'pekerjaan': 'Karyawan', 'penghasilan': 7000000, 'status': 'Disetujui'}
]

# Encode pekerjaan dan status
le_pekerjaan = LabelEncoder()
le_status = LabelEncoder()

# Mengubah pekerjaan dan status menjadi angka
pekerjaan = [entry['pekerjaan'] for entry in data_latihan]
status = [entry['status'] for entry in data_latihan]

# Fit encoder
le_pekerjaan.fit(pekerjaan)
le_status.fit(status)

# Persiapkan data pelatihan (X: fitur, y: target)
X = [
    [entry['umur'], le_pekerjaan.transform([entry['pekerjaan']])[0], entry['penghasilan']]
    for entry in data_latihan
]

y = le_status.transform(status)

# Melatih model Logistic Regression
model = LogisticRegression()
model.fit(X, y)

# Menyimpan model menggunakan joblib (untuk digunakan di masa mendatang)
joblib.dump(model, 'credit_card_model.pkl')
joblib.dump(le_pekerjaan, 'pekerjaan_encoder.pkl')
joblib.dump(le_status, 'status_encoder.pkl')

# Fungsi untuk prediksi apakah disetujui atau tidak
def prediksi_kartu_kredit(umur, pekerjaan, penghasilan):
    try:
        pekerjaan_encoded = le_pekerjaan.transform([pekerjaan])[0]
        prediksi = model.predict([[umur, pekerjaan_encoded, penghasilan]])[0]
        status = le_status.inverse_transform([prediksi])[0]
        return status
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")

# Endpoint untuk menerima data aplikasi kartu kredit
@router.post("/check")
def check_credit_application(application: CreditCardApplication):
    try:
        status = prediksi_kartu_kredit(application.umur, application.pekerjaan, application.penghasilan)
        return {"nama": application.nama, "status": status}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
