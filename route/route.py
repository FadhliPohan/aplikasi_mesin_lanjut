from fastapi import APIRouter
from app.controller.tugas1 import router as tugas1_router  # Mengimpor router dari controller tugas1
from app.controller.kartuDebitController import router as kartudebit_router  # Mengimpor router dari controller kartuDebit
from app.controller.deteksihewanController import router as deteksihewan_router  # Mengimpor router dari controller deteksihewan

# Membuat router utama
router = APIRouter()

# Menambahkan router tugas1 dengan prefix "/tugas1"
router.include_router(tugas1_router, prefix="/tugas1")

# Menambahkan router kartuDebit dengan prefix "/kartuDebit"
router.include_router(kartudebit_router, prefix="/kartuDebit")
router.include_router(deteksihewan_router, prefix="/deteksihewan")

# Menambahkan route utama
@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Menambahkan route greet dengan parameter nama
@router.get("/greet/{name}")
def read_greeting(name: str):
    return {"message": f"Hello, {name}!"}
