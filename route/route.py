from fastapi import APIRouter
from app.controller.tugas1 import router as tugas1_router  # Mengimpor router dari controller tugas1

router = APIRouter()  # Router untuk route utama

# Menambahkan router tugas1 dengan prefix "/tugas1"
router.include_router(tugas1_router, prefix="/tugas1")

# Menambahkan route lainnya
@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.get("/greet/{name}")
def read_greeting(name: str):
    return {"message": f"Hello, {name}!"}
